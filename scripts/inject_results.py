# note: run this from the root directory, not this directory
# so that it picks up the credential file

import os
import json
import re
from typing import Dict

from mnu_gsheets.gsheets import get_worksheet

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
    # print(mnu_url)
    mnu_ids = re.findall(r"(MIN[\d_]+)", mnu_url)
    if not mnu_ids:
        print(f"Couldn't extract info from {m_url} {mnu_url}")
        continue
    mnu_id = mnu_ids[0]
    id_map[mnu_id] = m_url

for row in raw_vals:
    mal_cell = row[3]
    mnu_id = row[0].value
    if mnu_id in id_map:
        if not mal_cell.value.strip():
            # linked cells update remote value
            mal_cell.value = id_map[mnu_id]
