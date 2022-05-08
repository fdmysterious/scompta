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
# │ Check undefined accounts               │
# └────────────────────────────────────────┘

def undefined_accounts(df, accs_df):
    """
    Checks which accounts are not defined from given dataframe.
    Returns the list of undefined acconut names, as well as the concerned transactions
    """

    # Transaction referring to unknown accounts
    tr_unknown_accounts = df.loc[~(df["from"].isin(accs_df.index) | df["to"].isin(accs_df.index))]

    tr_from             = tr_unknown_accounts["from"].rename("path")
    tr_to               = tr_unknown_accounts["to"  ].rename("path")

    # List of unknown accounts path
    l_unknown_accounts  = pd.merge(tr_from, tr_to, how="outer")

    return l_unknown_accounts, tr_unknown_accounts


# ┌────────────────────────────────────────┐
# │ Input/Output                           │
# └────────────────────────────────────────┘

def input(df, account_name: str):
    return df.loc[df["to"] == account_name]


def output(df, account_name: str):
    return df.loc[df["from"] == account_name]
