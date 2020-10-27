# TODO: automatically add based on MAL club IDs?

import time
from typing import Dict, Any

import backoff
import jikanpy

from .utils.backoff_gen import fibo_long

jikan = jikanpy.Jikan("http://localhost:8000/v3/")


@backoff.on_exception(fibo_long, jikanpy.APIException, max_tries=10)
def get_romaji(mal_id: int) -> str:
    resp: Dict[str, Any] = jikan.anime(mal_id)
    time.sleep(10)
    return str(resp["title"])
