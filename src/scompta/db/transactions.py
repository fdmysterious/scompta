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
