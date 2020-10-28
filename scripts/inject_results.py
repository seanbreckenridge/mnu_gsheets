import os
import json
import re
from typing import Dict

from mnu_gsheets.gsheets import get_worksheet, get_named_column

this_dir = os.path.dirname(os.path.abspath(__file__))

worksheet = get_worksheet(
    "client_secret.json", "1N4D3C0bSXVcVh0ggt_mpKMy_OrAdkKGkMjwkMekjpOM"
)
raw_vals = worksheet.get_all_values(returnas="range").cells

with open(os.path.join(this_dir, "results.json")) as f:
    results = json.load(f)

id_map: Dict[str, str] = {}

# clean ids, map mnu id to mal id
for m_url, mnu_url in results.items():
    mnu_ids = re.findall(r"(MIN[\d_]+)", mnu_url)
    if not mnu_ids:
        print("Couldnt extract anything from mnu_url")
        continue
    mnu_id = mnu_ids[0]
    id_map[mnu_id] = m_url

for row in raw_vals:
    mal_cell = row[3]
    mnu_id = row[0].value
    if mnu_id in id_map:
        # linked cells update remote value
        mal_cell.value = id_map[mnu_id]
