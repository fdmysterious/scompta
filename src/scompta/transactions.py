"""
┌────────────────────────────┐
│ Operations on transactions │
└────────────────────────────┘

 Florian Dupeyron
 May 2022
"""

import logging

import pandas as pd

from   pathlib import Path
from   money   import Money


# ┌────────────────────────────────────────┐
# │ Helper functions                       │
# └────────────────────────────────────────┘

def __money_conv(x):
    data = x.split(" ")
    currency = data[0]
    value    = data[1]

    return Money(value, currency)


# ┌────────────────────────────────────────┐
# │ Load and save from CSv                 │
# └────────────────────────────────────────┘

def load(fpath: Path):
    csv_data = pd.read_csv(str(fpath),
        sep=";",
        converters={
            "amount": __money_conv
        },
        skipinitialspace=True
    )

    # Check shape
    # TODO #

    return csv_data


def save(fpath: Path, df: pd.DataFrame):
    df.to_csv(str(fpath),
        sep=";",
        index=False
    )


# ┌────────────────────────────────────────┐
# │ Input/Output                           │
# └────────────────────────────────────────┘

def input(df, account_name: str):
    return df.loc[df["to"] == account_name]

def output(df, account_name: str):
    return df.loc[df["from"] == account_name]


