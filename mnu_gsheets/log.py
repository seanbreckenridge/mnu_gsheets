from os import environ
import logging
from logzero import setup_logger  # type: ignore[import]

logger = setup_logger(name="mnu_gsheets", level="DEBUG")
