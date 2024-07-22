from typing import Literal, Optional, Any, TypeAlias
import logging
import json

import requests
from retry import retry

import wbi

__all__ = ["get_video_detail", "get_video_stream_dash", "DEFAULT_HEADERS"]

_Params: TypeAlias = dict[str, str | int | float | bytes | bool]

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://www.bilibili.com/",
}
DEFAULT_TIMEOUT = 10

wbim = wbi.CachedWbiManager()


def _request_json(
    url: str,
    method: Literal["GET", "POST", "HEAD"] = "GET",
    session: Optional[requests.Session] = None,
    **kwargs,
) -> dict[str, Any]:
    session = session if session else requests.Session()
    kwargs.setdefault("headers", DEFAULT_HEADERS.copy())
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)

    with session.request(method=method, url=url, **kwargs) as resp:
        resp.raise_for_status()
        return resp.json()


def _c1fabvid(func):
    """
    "choose 1 from a/bvid"

    当没有从avid/bvid中选一个来传入时触发assert的装饰器
    """

    def abvchecker(avid: Optional[int] = None, bvid: Optional[str] = None, **kwargs):
        assert (avid is None) != (bvid is None), "Choose a/bvid to pass value"
        return func(avid=avid, bvid=bvid, **kwargs)

    return abvchecker


def _cbreturncode(func):
    """
    "check bili return code"

    检查函数的返回数据是否表现为成功，否则assert
    """

    def bilichecker(**kwargs):
        data = func(**kwargs)
        code = data.get("code")
        msg = data.get("message")
        if not msg:
            msg = data.get("msg")
        assert code == 0, msg
        return data

    return bilichecker


__NOTES_DECOPUZZLE_ANSW = """
这个最简单的装饰器：
其中用来包裹原始函数的函数会覆盖原始函数的名字、`docstring`等信息
以及什么都不管就悄咪咪地做无延时的无限重试，怎么想都会有问题罢

对于第一个问题，使用`functools.wraps`装饰新函数即可
对于第二个问题，添加更多机制即可，
    比如再在外面套一层函数用来返回装饰器函数，
    调用这个函数时就可以提供更多选项了。
"""


@_c1fabvid
@_cbreturncode
@retry(tries=3)
def get_video_detail(
    *,
    avid: Optional[int] = None,
    bvid: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> dict[str, Any]:
    """
    See https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/info.md#%E8%8E%B7%E5%8F%96%E8%A7%86%E9%A2%91%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AFweb%E7%AB%AF
    """
    api = "https://api.bilibili.com/x/web-interface/view"
    params: _Params = {}
    if bvid is not None:
        params["bvid"] = bvid
    if avid is not None:
        params["aid"] = avid

    return _request_json(api, method="GET", session=session, params=params)


@_c1fabvid
@_cbreturncode
@retry(tries=3)
def get_video_stream_dash(
    *,
    cid: int,
    avid: Optional[int] = None,
    bvid: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> dict[str, Any]:
    """
    See https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/videostream_url.md#fnval%E8%A7%86%E9%A2%91%E6%B5%81%E6%A0%BC%E5%BC%8F%E6%A0%87%E8%AF%86
    """
    api = "https://api.bilibili.com/x/player/wbi/playurl"
    params: _Params = {}
    if bvid is not None:
        params["bvid"] = bvid
    if avid is not None:
        params["avid"] = avid
    params.update(
        {
            "cid": cid,
            "fnval": 16 | 64 | 128 | 1024,
            "fourk": 1,
        }
    )
    params = wbim.sign(params)

    return _request_json(api, method="GET", session=session, params=params)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with open("./sample_detail.json", "w+", encoding="utf-8") as fp:
        json.dump(get_video_detail(avid=170001), fp, ensure_ascii=False, indent=4)
    with open("./sample_stream.json", "w+", encoding="utf-8") as fp:
        json.dump(
            get_video_stream_dash(cid=279786, avid=170001),
            fp,
            ensure_ascii=False,
            indent=4,
        )
