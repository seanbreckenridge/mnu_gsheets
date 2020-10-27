from typing import Union
from ..common import WorksheetRow, WorksheetData

import pygsheets  # type: ignore[import]

# https://stackoverflow.com/a/21231012
def column_to_letter(col: int) -> str:
    temp: Union[int, str] = 0
    letter: str = ""
    while col > 0:
        temp = (col - 1) % 26
        letter = chr(temp + 65) + letter
        col = (col - temp - 1) // 26
    return letter


def pad_data(data: WorksheetData, start_range: str, end_range: str) -> WorksheetData:
    """'data' is a list of lists which doesn't have equal inner lists,
    returns a list padded accordinding to the range
    """
    top_x, top_y = pygsheets.format_addr(start_range)
    bottom_x, bottom_y = pygsheets.format_addr(end_range)
    row_count: int = bottom_x - top_x + 1
    column_count: int = bottom_y - top_y + 1

    if row_count <= 0 or column_count <= 0:
        raise ValueError(
            f"Negative range recieved for range: '{start_range} -> {end_range}'"
        )

    initial_row_count: int = len(data)
    initial_col_count: int = max(map(len, data))

    if initial_row_count > row_count:
        raise ValueError(
            f"Row count for data ({initial_row_count}) exceeds row count defined by range ({row_count})"
        )

    if initial_col_count > column_count:
        raise ValueError(
            f"Max column count for data ({initial_col_count}) exceeds col count defined by range ({column_count})"
        )

    padded_data: WorksheetData = []

    for row in data:
        padded_row: WorksheetRow = []
        # add data that already exists
        for col in row:
            padded_row.append(col)
        # add extra spaces for each row
        while len(padded_row) < column_count:
            padded_row.append("")
        padded_data.append(padded_row)
    # add additional empty rows
    while len(padded_data) < row_count:
        padded_data.append(["" for _ in range(column_count)])
    return padded_data


# start range and end range are like 'A1' 'B10'
def update_sheet(
    worksheet: pygsheets.Worksheet,
    data: WorksheetData,
    start_range: str,
    end_range: str,
) -> None:
    worksheet.update_values(
        crange=f"{start_range}:{end_range}",
        values=pad_data(data, start_range, end_range),
    )
