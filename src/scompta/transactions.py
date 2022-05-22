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

from .         import accounts
from .accounts import Account_Type


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
    fpath = Path(fpath)

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
    df["amount"] = df["amount"].apply(lambda x: f"{x.currency} {x.amount}")
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

def input(df, df_accounts, account_names: str):
    accs = account_names
    if isinstance(accs, str):
        accs = [accs]

    if df_accounts is None:
        return df.loc[df["to"].isin(accs)]
    else:
        df_from = df_accounts.loc[df["from"]].reset_index()
        return df.loc[df["to"].isin(accs) & (df_from["type"] == Account_Type.Income)]


def output(df, df_accounts, account_names: str):
    accs = account_names
    if isinstance(accs, str):
        accs = [accs]
    
    if df_accounts is None:
        return df.loc[df["from"].isin(accs)]
    else:
        df_to = df_accounts.loc[df["to"]].reset_index()
        return df.loc[df["from"].isin(accs) & (df_to["type"] == Account_Type.Outcome)]
