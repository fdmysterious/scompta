"""
┌────────────────────┐
│ Views for accounts │
└────────────────────┘

 Florian Dupeyron
 October 2022
"""

from scompta.model.account import Account_Type

def with_type(df: tt: Account_Type):
    """
    Returns the list of accounts with the given type
    """

    return df.loc[df["type"] == tt]
