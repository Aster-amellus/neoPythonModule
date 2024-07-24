import os
import re
import subprocess
from typing import Any, Optional
from urllib import parse

import requests

import biliapis
import bilicodes

REGEX_BVID = re.compile(r"(BV[a-zA-Z0-9]{10})", re.I)
REGEX_AVID = re.compile(r"av([0-9]+)", re.I)


def extract_ids(s: str) -> dict[str, int | str]:
    bvids = REGEX_BVID.findall(s)
    avids = REGEX_AVID.findall(s)
    ids = {}
    if bvids:
        ids["bvid"] = bvids[0]
    elif avids:
        ids["avid"] = int(avids[0])
    return ids


def normalize_filename(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*]', " ", s)
    s = s.strip()
    s = re.sub(r"\s+", "_", s)
    if not s:
        s = "filename"
    return s


def make_choice(
    text: str, options: list[str], spec_options: Optional[dict[str, str]] = None
) -> str | int | None:
    """让用户做出选择的函数"""
    # print options
    if not options and not spec_options:
        print("No options to choose")
        return None
    print(text)
    for i, opt in enumerate(options):
        print("({:>2}) {}".format(i, opt))
    if spec_options:
        for k, opt in spec_options.items():
            print("({}) {}".format(k, opt))
    while True:
        try:
            choice = input("Choice:").strip()
        except KeyboardInterrupt:
            return None
        if choice.isdigit() and options:
            if int(choice) in range(len(options)):
                return int(choice)
        if spec_options:
            if choice in spec_options.keys():
                return choice


def get_filename(url: str, session: Optional[requests.Session] = None, **kwargs) -> str:
    """从URL获取文件名"""
    # 尝试请求
    kwargs.setdefault("timeout", 10)
    session = session if session else requests.Session()
    with session.head(url, **kwargs) as resp:
        if resp.status_code == 200:
            if cd := resp.headers.get("Content-Disposition"):
                filenames = re.findall('filename="(.+?)"', cd)
                if filenames:
                    return filenames[0]
    # 直接切分
    filename = parse.urlparse(url).path.split("/")[-1]
    filename = filename.split("?")[0].split("#")[0]
    return parse.unquote(filename)


def download(
    url: str,
    save_dir: str,
    filename: Optional[str] = None,
    session: Optional[requests.Session] = None,
    chunk_size: int = 4096,
    **kwargs,
):
    kwargs.setdefault("timeout", 10)
    session = session if session else requests.Session()
    if not filename:
        filename = get_filename(url, session=session, **kwargs)
    filename = normalize_filename(filename)
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "wb+") as fp:
        with session.get(url, stream=True, **kwargs) as resp:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    fp.write(chunk)


def merge_avfile(au_file: str, vi_file: str, output_file: str) -> int:
    """调用ffmpeg进行合流"""
    # fmt: off
    cmd = [
        "ffmpeg", "-loglevel", "quiet", "-nostdin", "-hide_banner",
        "-i", au_file, "-i", vi_file,
        "-vcodec", "copy", "-acodec", "copy",
        output_file
    ]
    # fmt: on
    # 上面那对注释是临时关闭 black 格式化，它会把命令行列表展开成一长条反而不好看
    with subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as subp:
        return subp.wait()


def generate_filename(
    video_data: dict[str, Any],
    video_stream: dict[str, Any],
    audio_stream: dict[str, Any],
    part_index: int = 0,
) -> tuple[str, str, str]:
    """生成下载文件名

    Args:
        video_data (dict[str, Any]): 视频本体数据
        video_stream (dict[str, Any]): 视频流数据（单个流）
        audio_stream (dict[str, Any]): 音频流数据（单个流）
        part_index (int, optional): 视频分P索引，注意与`video_stream`保持一致. Defaults to 0.

    Returns:
        tuple[str, str, str]: 视频流, 音频流, 最终文件名
    """
    if "code" in video_data and "data" in video_data:
        video_data = video_data["data"]
    page: dict[str, Any] = video_data["pages"][part_index]

    vstream_fn = "{cid}_{bandwidth}_videostream.m4v".format(**page, **video_stream)
    astream_fn = "{cid}_{bandwidth}_audiostream".format(**page, **audio_stream)
    astream_fn += ".flac" if audio_stream["id"] == 30251 else ".m4a"
    final_fn = "{title}_{bvid}_P{part_index}".format(
        **video_data, part_index=part_index + 1
    )
    if video_data["title"] != page["part"]:
        final_fn += "_" + page["part"]
    final_fn += "_" + bilicodes.stream_dash_video_quality[video_stream["id"]]
    final_fn += ".mkv" if audio_stream["id"] == 30251 else ".mp4"
    return vstream_fn, astream_fn, normalize_filename(final_fn)


def main():
    source = input("Input video source:")
    ids = extract_ids(source)
    if not ids:
        print("No valid id found.")
        return
    video_data = biliapis.get_video_detail(**ids)["data"]
    print(video_data["title"], "by", video_data["owner"]["name"])
    pindex = 0
    if len(video_data["pages"]) > 1:
        choice = make_choice(
            "多个分P，选择想要的", [i["part"] for i in video_data["pages"]]
        )
        if isinstance(choice, int):
            pindex = choice
        elif isinstance(choice, str):
            print("Unexpected choice, set to default 0")
        else:
            print("Aborted.")
            return
    else:
        print("仅有一个分P")
    cid = video_data["pages"][pindex]["cid"]
    print("正在取流")
    streams = biliapis.get_video_stream_dash(cid=cid, **ids)["data"]

    vstreams = streams["dash"]["video"]
    astreams = streams["dash"]["audio"]
    choice = make_choice(
        "选择想要的画质",
        [
            "{} - {} - {} bps".format(
                bilicodes.stream_dash_video_quality[i["id"]],
                bilicodes.stream_video_codec_codes[i["codecid"]],
                i["bandwidth"],
            )
            for i in vstreams
        ],
        {"max": "最大带宽", "min": "最小带宽"},
    )
    if isinstance(choice, int):
        vstream = vstreams[choice]
    elif isinstance(choice, str):
        if choice == "min":
            vstream = min(vstreams, key=lambda x: x["bandwidth"])
        else:
            vstream = max(vstreams, key=lambda x: x["bandwidth"])
    else:
        print("Aborted.")
        return
    astream = max(astreams, key=lambda x: x["bandwidth"])

    vf, af, ff = generate_filename(video_data, vstream, astream, pindex)
    output_dir = input("Output to:").strip()
    if not os.path.isdir(output_dir):
        print("Not a dir. Aborted.")
        return

    download(vstream["base_url"], output_dir, vf, headers=biliapis.DEFAULT_HEADERS)
    download(astream["base_url"], output_dir, af, headers=biliapis.DEFAULT_HEADERS)
    merge_avfile(af, vf, ff)
    os.remove(vf)
    os.remove(af)
    print("Complete.")


if __name__ == "__main__":
    main()
