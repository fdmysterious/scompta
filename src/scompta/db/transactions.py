"""
┌────────────────────────────────────────────┐
│ Helper to load transactions from CSV files │
└────────────────────────────────────────────┘

 Florian Dupeyron
 October 2022
"""

import logging
import pandas as pd


from pathlib import Path
from money   import Money

from scompta.model.account     import Account_Type
from scompta.model.transaction import Transaction

log = logging.getLogger(__file__)


# ┌────────────────────────────────────────┐
# │ Helpers                                │
# └────────────────────────────────────────┘

def __money_conv(x):
    data     = x.split(" ")
    currency = data[0]
    value    = data[1]

    return Money(value, currency)


# ┌────────────────────────────────────────┐
# │ Load and save from CSV                 │
# └────────────────────────────────────────┘

def load(fpath: Path):
    fpath = Path(fpath)

    csv_data = pd.read_csv(str(fpath),
        sep=";",
        converters={
            "amount": __money_conv
        },

        skipinitialspace=True
    )

    # Check shape?
    # TODO

    return csv_data


def save(fpath: Path, df: pd.DataFrame):
    df["amount"] = df["amount"].apply(lambda x: f"{x.currency} {x.amount}")
    df.to_csv(str(fpath),
        sep=";",
        index=False
    )


# ┌────────────────────────────────────────┐
# │ Create from boilerplate                │
# └────────────────────────────────────────┘

def create(fpath: Path):
    """
    Create boilerplace CSV file for transaction list
    """
    log.info("Initialize transactions list in {fpath}")
    fpath.write_text("day;time;label;origin;target;amount;tag")
