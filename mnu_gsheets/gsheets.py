from typing import List, Any

import pygsheets  # type: ignore[import]

from .request_mnu import MnuData


def authorize(secret: str) -> pygsheets.client.Client:
    return pygsheets.authorize(client_secret=secret)


def update_sheets(
    secret_file: str, spreadsheet_id: str, mnu_data: List[MnuData]
) -> None:
    # authentication flow happens if needed
    gc = authorize(secret_file)
    # TODO: request remote and populate set difference
