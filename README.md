# mnu_gsheets

This indexes existing [_minna no uta_](https://en.wikipedia.org/wiki/Minna_no_Uta) entries every couple days, adding rows for ones that don't exist to the spreadsheet, so that they can be added to online databases.

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
# create a spreadsheet and name the target worksheet 'Index'
mnu_gsheets update --sid 1N4D.... --creds ./client_secret.json
```

I use the `update` script to do the above

### TODO:

- show images using proxy
- data validation
