import re
from datetime import date
from typing import List, Set, Optional

import pygsheets  # type: ignore[import]

from .request_mnu import MnuData
from .utils.gsheet_utils import update_sheet, column_to_letter
from .constants import worksheet_title, header_info, frozen_rows
from .common import WorksheetData, WorksheetRow, WorksheetValue
from .mal import get_romaji
from .log import logger

LIVE_ACTION = "実写"


def get_named_column(row: WorksheetRow, column_name: str) -> WorksheetValue:
    assert column_name in header_info, "unknown column_name: {}".format(column_name)
    return row[header_info.index(column_name)]


def _format_date(d: Optional[date]) -> str:
    """
    Format the date into the google sheet format
    """
    if d is None:
        return ""
    return d.strftime("=DATE(%Y,%m,%d)")


def _format_credits(cs: str) -> str:
    """
    Format credits data into a search link, if possible
    """
    # no data
    if not cs.strip():
        return ""
    # multiple artists, cant search
    elif "｜" in cs:
        return cs
    else:
        search_link: str = (
            r"https://www.nhk.or.jp/minna/search/?keyword={}&opt=all".format(cs)
        )
        return f'=HYPERLINK("{search_link}", "{cs}")'


def create_mnu_row(mdat: MnuData) -> WorksheetRow:
    """
    Convert requested MnU data into a Google Sheet row
    """
    return list(
        map(
            str.strip,
            [
                mdat.mnu_id,
                f'=HYPERLINK("{mdat.link}", "{mdat.link}")',
                "",  # no romaji by default
                "",  # mal
                "N",
                mdat.title,
                f'=HYPERLINK("{mdat.image_link}", "{mdat.image_link}")',
                mdat.kana,
                mdat.body_text,
                _format_credits(mdat.credits.singer),  # song performance
                _format_credits(mdat.credits.writing),  # lyrics
                _format_credits(mdat.credits.composition),
                _format_credits(mdat.credits.arrangement),
                _format_credits(mdat.credits.picture),
                _format_date(mdat.broadcast_start),
                _format_date(mdat.broadcast_end),
                "",  # live action: 1
                "Y"
                if LIVE_ACTION == mdat.credits.picture.strip()
                else "",  # live action: 2
            ],
        )
    )


def get_worksheet(secret_file: str, spreadsheet_id: str) -> pygsheets.Worksheet:
    # authentication flow happens if needed
    gc = pygsheets.authorize(client_secret=secret_file)

    # get references to worksheet
    spreadsheet: pygsheets.Spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet: pygsheets.Worksheet = spreadsheet.worksheet_by_title(worksheet_title)
    return worksheet


def update(
    secret_file: str,
    spreadsheet_id: str,
    mnu_data: List[MnuData],
    skip_romaji: bool = False,
) -> None:
    # setup
    worksheet = get_worksheet(secret_file, spreadsheet_id)
    worksheet.frozen_rows = frozen_rows
    update_sheet(
        worksheet, [header_info], "A2", f"{column_to_letter(len(header_info))}2"
    )

    # get all values
    raw_vals: WorksheetData = worksheet.get_all_values(returnas="matrix")

    # drop empty rows
    all_vals: WorksheetData = []
    for row in raw_vals:
        if "".join(row).strip():
            all_vals.append(row)

    # get all the IDs that are already on the sheet
    ids_in_worksheet: Set[str] = set(
        [get_named_column(row, "MnU ID") for row in all_vals[frozen_rows:]]
    )

    # create a list of any new IDs
    new_vals: WorksheetData = []
    for mdat in mnu_data:
        # if not already on the spreadsheet
        if mdat.mnu_id not in ids_in_worksheet:
            # create corresponding row
            logger.info("Adding {} to spreadsheet".format(mdat.mnu_id))
            new_vals.append(create_mnu_row(mdat))

    # if there are any new rows to add
    if new_vals:
        top_row = len(all_vals) + 1
        last_column: str = column_to_letter(len(header_info))
        bottom_row: int = len(all_vals) + len(new_vals)

        update_sheet(worksheet, new_vals, f"A{top_row}", f"{last_column}{bottom_row}")

    # if any MAL links have been addded which dont have corresponding Romaji
    if not skip_romaji:
        all_cells: WorksheetData = worksheet.get_all_values(returnas="range").cells
        for row in all_cells:
            romaji_cell: pygsheets.Cell = get_named_column(row, "Romaji")
            mal_cell: pygsheets.Cell = get_named_column(row, "MyAnimeList")
            # if MAL has value, but romaji is empty
            if mal_cell.value.strip() and not romaji_cell.value.strip():
                logger.info(
                    "Requesting romaji for {}...".format(mal_cell.value.strip())
                )
                try:
                    romaji_text: str = get_romaji(
                        re.findall("anime/(\d+)", mal_cell.value)[0]
                    )
                except Exception as e:
                    logger.exception(e)
                    continue
                # linked cell updates remote value
                romaji_cell.value = romaji_text
