import os
import json
from datetime import date
from typing import List, Dict, Any, NamedTuple, Optional, Iterator

import requests
from cachecontrol import CacheControl  # type: ignore[import]
from cachecontrol.heuristics import ExpiresAfter  # type: ignore[import]
from cachecontrol.caches.file_cache import FileCache  # type: ignore[import]

from . import cache_dir
from .log import logger
from .utils.user_agent import random_user_agent

session = requests.Session()
session.headers.update({"User-Agent": random_user_agent()})
cachesession = CacheControl(
    session,
    heuristic=ExpiresAfter(days=1),
    cache=FileCache(os.path.join(cache_dir, "requests")),
)

INDEX = "https://www.nhk.or.jp/minna/request/index.json"


class MnuCredits(NamedTuple):
    singer: str
    writing: str
    composition: str
    arrangement: str
    picture: str


class MnuData(NamedTuple):
    mnu_id: str
    image: str
    title: str
    kana: str
    body_text: str
    credits: MnuCredits
    date_start: Optional[date]
    date_end: Optional[date]

    def link(self) -> str:
        return "https://www.nhk.or.jp/minna/songs/{}".format(self.mnu_id)


def _parse_date(ds: str) -> Optional[date]:
    try:
        year, month, day = list(map(int, ds.split("/")))
        return date(year=year, month=month, day=day)
    except Exception as e:
        logger.warning(str(e))
        return None


def parse_request(d: Dict[str, Any]) -> MnuData:
    return MnuData(
        mnu_id=d["keyname"],
        title=d["title"],
        kana=d["kana"],
        body_text=d["body"],
        image=d["image"],
        credits=MnuCredits(
            singer=d["credit"]["singer"],
            writing=d["credit"]["writing"],
            composition=d["credit"]["composition"],
            arrangement=d["credit"]["arrangement"],
            picture=d["credit"]["picture"],
        ),
        date_start=_parse_date(d["date_start"]),
        date_end=_parse_date(d["date_end"]),
    )


def request_mnu_data() -> Iterator[MnuData]:
    """
    Request info from the NHK website
    """
    resp: requests.Response = cachesession.get(INDEX)
    yield from map(parse_request, resp.json()["items"])
