"""
┌────────────────────────────────────┐
│ Helpers for periods in directories │
└────────────────────────────────────┘

 Florian Dupeyron
 May 2022
"""

import logging
import re

from pathlib import Path

log = logging.getLogger(__file__)

__RE_PERIOD_NAME = re.compile(r'[0-9]{4}-[0-9]{2}')

def list_from_dir(fpath: Path):
    """
    Return the list of periods from one given directory
    """
    return tuple(filter(lambda x: x.is_dir() and __RE_PERIOD_NAME.match(x.name), fpath.glob("*")))
