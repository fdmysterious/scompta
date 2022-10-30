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


# ┌────────────────────────────────────────┐
# │ Helpers                                │
# └────────────────────────────────────────┘

def load_from_dir(path: Path):
    """
    Loads the account hierarchy from given folder. Returns a DataFrame
    containing the account rows.
    """
    path = Path(path)

    log.info(f"Load accounts from path: {path}")

    r = []
    for fpath in path.glob("**/*.toml"):
        log.debug(f"Processing account data from {fpath}")
        try:
            # Get account path
            acc_path = str(fpath.parent.relative_to(path) / fpath.stem)

            # Create account object
            with open(fpath) as fhandle:
                # Get and process data
                acc_data = toml.load(fhandle)["account"]
                if "type" in acc_data:
                    acc_data["type"] = Account_Type(acc_data["type"])

                # Add account to list
                acc = Account(path=acc_path, **acc_data)
                r.append(acc)

        except Exception as exc:
            log.warn(f"Failed to process account data from {fpath}, Skipping")
            log.warn(traceback.format_exc())

    return pd.DataFrame(r).set_index("path")

