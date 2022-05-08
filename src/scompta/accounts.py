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

from dataclasses import dataclass, field, asdict
from enum        import Enum
from pathlib     import Path

log = logging.getLogger("SCompta Accounts")


# ┌────────────────────────────────────────┐
# │ Account types                          │
# └────────────────────────────────────────┘

class Account_Type(Enum):
    Liabilities = "liabilities"
    Assets      = "assets"
    Equity      = "equity"

    Income      = "income"
    Outcome     = "outcome"


# ┌────────────────────────────────────────┐
# │ Accounts dataclass                     │
# └────────────────────────────────────────┘

@dataclass
class Account:
    path: str
    name: str
    type: Account_Type


# ┌────────────────────────────────────────┐
# │ Helpers                                │
# └────────────────────────────────────────┘

def load_from_dir(path: Path):
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

