"""
┌──────────────────────────────────┐
│ Accounts loading from toml files │
└──────────────────────────────────┘

 Florian Dupeyron
 October 2022
"""

import logging
import traceback

import toml
import pandas as pd

from dataclasses import asdict

from pathlib import Path

from scompta.model.account import (
    Account,
    Account_Type
)

log = logging.getLogger(__file__)


# ┌────────────────────────────────────────┐
# │ Load from directory                    │
# └────────────────────────────────────────┘

def load_from_file(path: Path, acc_path):
    """
    Load account info. from file. Return a Account
    dataclass
    """
    path = Path(path)

    log.debug(f"Load account information from {path}'")

    with open(path) as fhandle:
        # Get and process data
        acc_data = toml.load(fhandle)["account"]
        if "type" in acc_data:
            acc_data["type"] = Account_Type(acc_data["type"])

        # Return account information
        return Account(path=acc_path, **acc_data)

def load_from_dir(root_path: Path):
    """
    Loads the account hierarchy from given folder. Returns a DataFrame
    containing the account rows
    """
    root_path = Path(root_path)

    def load_acc(fpath):
        try:
            # Get account relative path name
            acc_path = str(fpath.parent.relative_to(root_path) / fpath.stem)

            # Load account object
            return load_from_file(fpath, acc_path)
        except Exception as exc:
            log.warn(f"Failed to process data from {fpath}, Skipping")
            log.warn(traceback.format_exc())

    log.info(f"Load accounts from path: {root_path}")

    accs_gen = map(load_acc, root_path.glob("**/*.toml"))

    return pd.DataFrame(accs_gen).set_index("path")


# ┌────────────────────────────────────────┐
# │ Save to file                           │
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

