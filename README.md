# mnu_gsheets

WIP

tracking obscure anime music videos

## Installation

Requires `python3.7+`

To install:

Expects Jikan to be running on port 8000; [docker](https://github.com/seanbreckenridge/docker-jikan)

```bash
# clone and cd to this directory
pip install .
# follow instructions to setup google sheets
# https://pygsheets.readthedocs.io/en/staging/authorization.html
# put secret file in ./client_secret.json
# create a spreadsheet with header structure similar to https://docs.google.com/spreadsheets/d/1N4D3C0bSXVcVh0ggt_mpKMy_OrAdkKGkMjwkMekjpOM
mnu_gsheets update --sid 1N4D.... --creds ./client_secret.json
```
