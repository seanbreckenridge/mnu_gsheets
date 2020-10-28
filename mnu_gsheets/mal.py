# TODO: automatically add based on MAL club IDs?

import time

import backoff  # type: ignore[import]
import jikanpy

from .utils.backoff_gen import fibo_long
from .common import Json

jikan = jikanpy.Jikan("http://localhost:8000/v3/")


@backoff.on_exception(fibo_long, jikanpy.APIException, max_tries=10)
def get_romaji(mal_id: int) -> str:
    resp: Json = jikan.anime(mal_id)
    time.sleep(5)
    return str(resp["title"])
