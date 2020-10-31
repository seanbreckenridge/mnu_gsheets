from typing import Dict, Any, List, Union
from pygsheets import Cell  # type: ignore[import]

Json = Dict[str, Any]
WorksheetValue = Union[str, Cell]
WorksheetRow = List[WorksheetValue]
WorksheetData = List[WorksheetRow]
