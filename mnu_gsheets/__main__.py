import json
from typing import List

import click

from .request_mnu import request_mnu_json, request_mnu_data, MnuData
from .gsheets import update as gsheets_update


@click.group()
def main() -> None:
    pass


@main.command()
def dump_mnu() -> None:
    """
    Print the cached MnU index as JSON to STDOUT
    """
    click.echo(json.dumps(request_mnu_json()))


@main.command()
@click.option(
    "--creds", type=click.Path(exists=True), help="client_secret.json credential file"
)
@click.option("--sid", type=str, help="google spreadsheet id")
@click.option(
    "--skip-romaji", is_flag=True, default=False, help="Skip downloading romaji"
)
def update(creds: str, sid: str, skip_romaji: bool) -> None:
    """
    Update the spreadsheet with any new entries.

    Download new info from the index if we haven't already
    done so in the last day. Push any new IDs to the spreadsheet
    """
    mnu: List[MnuData] = list(request_mnu_data())
    gsheets_update(creds, sid, mnu, skip_romaji)

if __name__ == "__main__":
    main(prog_name="mnu_gsheets")
