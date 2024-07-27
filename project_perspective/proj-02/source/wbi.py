"""
Original from 

https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md#python 

, Reorganized.
"""

from functools import reduce
from hashlib import md5
import urllib.parse
import time
from typing import Optional
from threading import Lock

import requests

__all__ = ["CachedWbiManager", "sign", "get_wbi_keys"]

# fmt: off
MIXINKEY_ENC_TABLE = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]
# fmt: on


class CachedWbiManager:
    def __init__(self) -> None:
        self.img_key_cache: Optional[str] = None
        self.sub_key_cache: Optional[str] = None
        self._last_cache_fetch: float = 0
        self._keys_refresh_lock = Lock()
        self.cache_refresh_limit = 1 * 60 * 60

    def get_cached_keys(self):
        if (
            time.time() - self._last_cache_fetch < self.cache_refresh_limit
            and self.img_key_cache
            and self.sub_key_cache
        ):
            return self.img_key_cache, self.sub_key_cache
        with self._keys_refresh_lock:
            self.img_key_cache, self.sub_key_cache = get_wbi_keys()
            self._last_cache_fetch = time.time()
        return self.img_key_cache, self.sub_key_cache

    def sign(self, params: dict):
        img_key, sub_key = self.get_cached_keys()
        return sign(params=params, img_key=img_key, sub_key=sub_key)


def _get_mixinkey(orig: str):
    "对 imgKey 和 subKey 进行字符顺序打乱编码"
    return reduce(lambda s, i: s + orig[i], MIXINKEY_ENC_TABLE, "")[:32]


def sign(params: dict, img_key: str, sub_key: str):
    "为请求参数进行 wbi 签名"
    params = params.copy()
    mixin_key = _get_mixinkey(img_key + sub_key)
    curr_time = round(time.time())
    params["wts"] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params["w_rid"] = wbi_sign
    return params


def get_wbi_keys() -> tuple[str, str]:
    "获取最新的 img_key 和 sub_key"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Referer": "https://www.bilibili.com/",
    }
    with requests.get(
        "https://api.bilibili.com/x/web-interface/nav", headers=headers, timeout=10
    ) as resp:
        resp.raise_for_status()
        json_content = resp.json()
    img_url: str = json_content["data"]["wbi_img"]["img_url"]
    sub_url: str = json_content["data"]["wbi_img"]["sub_url"]
    img_key = img_url.rsplit("/", 1)[1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
    return img_key, sub_key


if __name__ == "__main__":
    manager = CachedWbiManager()
    signed_params = manager.sign(params={"foo": "114", "bar": "514", "baz": 1919810})
    print(signed_params)
