"""
┌────────────────────┐
│ Accounts managment │
└────────────────────┘

 Florian Dupeyron
 May 2022
"""

import logging
import traceback

import toml
import pandas as pd

from itertools   import chain
from dataclasses import dataclass, field, asdict
from enum        import Enum
from pathlib     import Path
from typing      import Optional

from .model.account import (
    Account,
    Account_Type,
)

log = logging.getLogger("SCompta Accounts")


# ┌────────────────────────────────────────┐
# │ Load/Save/Create                       │
# └────────────────────────────────────────┘

def save(account: Account, fpath: Path):

    acc_path = fpath / f"{account.path}.toml"
    log.info(f"Save account {account.name} to {acc_path}")

    # Compute base directory path
    basedir = (acc_path / "..").resolve()

    # Create basedir if it doesn't exist
    if not basedir.exists():
        log.info("Create directory {basedir}")
        basedir.mkdir(parents=True)

    # Save to file
    with open(acc_path, "w") as fhandle:
        data = asdict(account)
        del data["path"]

        toml.dump({"account": data}, fhandle)


# ┌────────────────────────────────────────┐
# │ Operations on Accounts DataFrame       │
# └────────────────────────────────────────┘


def with_type(df, tt: Account_Type):
    return df.loc[df["type"] == tt]
