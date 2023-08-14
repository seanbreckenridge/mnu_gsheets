import orjson
from pathlib import Path
from typing import Dict, Any, List
from .gsheets import ExportData, export
from .request_mnu import MnuData, request_mnu_data


def _orjson_default(obj: Any) -> Any:
    if hasattr(obj, "_asdict"):
        return obj._asdict()
    else:
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )


def combine_export(secret_file: str, spreadsheet_id: str, output_dir: str) -> None:
    export_data: List[ExportData] = export(secret_file, spreadsheet_id)
    mnu_data: Dict[str, MnuData] = {mnu.mnu_id: mnu for mnu in request_mnu_data()}

    combined: Dict[str, Any] = {}

    for row in export_data:
        assert row.mnu_id not in combined

        combined[row.mnu_id] = {
            "spreadsheet_data": row,
            "mnu_data": mnu_data[row.mnu_id],
        }

    out_dir = Path(output_dir)
    with open(out_dir / "mnu_export.json", "wb") as fo:
        # write as JSON
        fo.write(orjson.dumps(list(combined.values()), default=_orjson_default))
