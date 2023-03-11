"""
┌────────────────────┐
│ Transactions model │
└────────────────────┘

 Florian Dupeyron
 October 2022
"""

from money       import Money

from .account    import Account
from .account    import Account_Type

from dataclasses import dataclass

from typing      import Optional


# ┌────────────────────────────────────────┐
# │ Main trasaction dataclass              │
# └────────────────────────────────────────┘

@dataclass
class Transaction:
    day: int
    time: str

    origin: str
    target: str
    amount: Money

    label: Optional[str]
    tag: Optional[str]
