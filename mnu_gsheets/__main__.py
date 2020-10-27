import click
from typing import List
from pathlib import Path

from .request_mnu import request_mnu_data, MnuData
from .gsheets import update_sheets


@click.group()
def main() -> None:
    pass


@main.command()
@click.option(
    "--creds", type=click.Path(exists=True), help="client_secret.json credential file"
)
@click.option("--sid", type=str, help="google spreadsheet id")
def update(creds: str, sid: str) -> None:
    mnu: List[MnuData] = list(request_mnu_data())
    update_sheets(creds, sid, mnu)
