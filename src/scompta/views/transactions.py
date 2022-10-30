"""
┌────────────────────────┐
│ Views for transactions │
└────────────────────────┘

 Florian Dupeyron
 October 2022
"""

import logging

import pandas as pd

from pathlib import Path
from money   import Money

from scompta.model.account import (
    Account_Type
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
    tr_unknown_accounts = df.loc[~(df["origin"].isin(accs_df.index) | df["target"].isin(accs_df.index))]

    tr_from             = tr_unknown_accounts["origin"].rename("path")
    tr_to               = tr_unknown_accounts["target"].rename("path")

    # List of unknown accounts path
    l_unknown_accounts  = pd.merge(tr_from, tr_to, how="outer")

    return l_unknown_accounts, tr_unknown_accounts


# ┌────────────────────────────────────────┐
# │ Input/Output                           │
# └────────────────────────────────────────┘

def input(df, df_accounts, account_names: str):
    """
    List transactions that add money to the given accounts
    """

    accs = account_names
    if isinstance(accs, str):
        accs = [accs]

    if df_accounts is None:
        return df.loc[df["target"].isin(accs)]
    else:
        df_from = df_accounts.loc[df["origin"]].reset_index()
        return df.loc[df["target"].isin(accs) & (df_from["type"] == Account_Type.Income)]


def output(df, df_accounts, account_names: str):
    """
    List transactions that retrieve money from the given accounts
    """

    accs = account_names
    if isinstance(accs, str):
        accs = [accs]
    
    if df_accounts is None:
        return df.loc[df["origin"].isin(accs)]
    else:
        df_to = df_accounts.loc[df["target"]].reset_index()
        return df.loc[df["origin"].isin(accs) & (df_to["type"] == Account_Type.Outcome)]
