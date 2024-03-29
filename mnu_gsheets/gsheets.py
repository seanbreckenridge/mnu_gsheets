from datetime import date, datetime
from typing import List, Set, Optional, NamedTuple

import pygsheets  # type: ignore[import]

from .types import WorksheetData, WorksheetRow, WorksheetValue
from .request_mnu import MnuData
from .constants import worksheet_title, header_info, frozen_rows
from .log import logger
from .utils.gsheet_utils import update_sheet, column_to_letter

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
    # multiple artists, can't search
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
                "",  # no source
                "",  # no quality
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
    gc = pygsheets.authorize(client_secret=secret_file, local=True)

    # get references to worksheet
    spreadsheet: pygsheets.Spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet: pygsheets.Worksheet = spreadsheet.worksheet_by_title(worksheet_title)
    return worksheet


def update(
    secret_file: str,
    spreadsheet_id: str,
    mnu_data: List[MnuData],
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
        worksheet.rows += len(new_vals)

        update_sheet(worksheet, new_vals, f"A{top_row}", f"{last_column}{bottom_row}")

    worksheet.sort_range(
        start=f"A{frozen_rows + 1}",
        end=f"{column_to_letter(len(header_info))}{worksheet.rows}",
        sortorder="DESCENDING",
    )

    worksheet.update_value("A1", "Last Updated: " + str(datetime.now()).split(".")[0])


class ExportData(NamedTuple):
    """
    Useful information from the google sheet that's not already in the MnuData blobs

    this will be attached to the MnuData blobs
    """

    mnu_id: str
    romaji: str
    mal: str
    source_archived: str
    quality: str
    assumed_live_action: str
    confirm_live_action: str


def export(secret_file: str, spreadsheet_id: str) -> List[ExportData]:
    """
    Extract all the useful information from the google sheet
    """

    worksheet = get_worksheet(secret_file, spreadsheet_id)
    worksheet.frozen_rows = frozen_rows

    # get all values
    raw_vals: WorksheetData = worksheet.get_all_values(returnas="matrix")

    # parse the data
    return [
        ExportData(
            mnu_id=get_named_column(row, "MnU ID"),
            romaji=get_named_column(row, "Romaji"),
            mal=get_named_column(row, "MyAnimeList"),
            source_archived=get_named_column(row, "Source Archived"),
            quality=get_named_column(row, "Quality"),
            assumed_live_action=get_named_column(row, "Assume Live Action"),
            confirm_live_action=get_named_column(row, "Confirm Live Action"),
        )
        for row in raw_vals[frozen_rows:]
    ]
