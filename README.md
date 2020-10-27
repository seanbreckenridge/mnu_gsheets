# mnu_gsheets

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
# create a spreadsheet and name the target worksheet 'Index'
mnu_gsheets update --sid 1N4D.... --creds ./client_secret.json
```

I use the `update` script to do the above

### TODO:

- show images using proxy
- data validation
