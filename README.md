# mnu_gsheets

This indexes existing [_minna no uta_](https://en.wikipedia.org/wiki/Minna_no_Uta) entries every couple days, adding rows for ones that don't exist to the spreadsheet, so that they can be added to online databases.

## Installation

Requires `python3.7+`

To install:

```bash
# clone and cd to this directory
git clone https://github.com/seanbreckenridge/mnu_gsheets
cd mnu_gsheets
# install dependencies
pip install pipenv
pipenv install
pipenv shell
# follow instructions to setup google sheets
# https://pygsheets.readthedocs.io/en/staging/authorization.html
# put secret file in ./client_secret.json
# create a spreadsheet and name the target worksheet 'Index'
python3 -m mnu_gsheets update --sid 1N4D.... --creds ./client_secret.json
```

I use the `update` script to do the above

I also upload an export of this whenever I update it, to a public directory on my website: <https://sean.fish/p/mnu_exports/>
