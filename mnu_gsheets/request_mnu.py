import os
from datetime import date
from typing import List, NamedTuple, Optional, Iterator

import requests
from cachecontrol import CacheControl  # type: ignore[import]
from cachecontrol.heuristics import ExpiresAfter  # type: ignore[import]
from cachecontrol.caches.file_cache import FileCache  # type: ignore[import]

from . import cache_dir
from .log import logger
from .utils.user_agent import random_user_agent
from .common import Json

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
    broadcast_start: Optional[date]
    broadcast_end: Optional[date]

    @property
    def link(self) -> str:
        return "https://www.nhk.or.jp/minna/songs/{}".format(self.mnu_id)

    @property
    def image_link(self) -> str:
        return "https://www.nhk.or.jp" + self.image


def _parse_date(ds: str) -> Optional[date]:
    try:
        year, month, day = list(map(int, ds.split("/")))
        return date(year=year, month=month, day=day)
    except Exception as e:
        logger.warning(str(e))
        return None


def parse_json_entry(d: Json) -> MnuData:
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
        broadcast_start=_parse_date(d["date_start"]),
        broadcast_end=_parse_date(d["date_end"]),
    )


def request_mnu_json() -> List[Json]:
    logger.debug("Starting request...")
    resp_json: List[Json] = cachesession.get(INDEX).json()["items"]
    logger.debug("Finished request!")
    return resp_json


def request_mnu_data() -> Iterator[MnuData]:
    """
    Request info from the NHK website
    """
    yield from map(parse_json_entry, request_mnu_json())
