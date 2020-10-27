import os
import appdirs  # type: ignore[import]

# cache dir to store requests any any other info
cache_dir = appdirs.user_cache_dir("mnu_gsheets", "seanbreckenridge")
os.makedirs(cache_dir, exist_ok=True)
