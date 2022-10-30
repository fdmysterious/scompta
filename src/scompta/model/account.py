"""
┌────────────────┐
│ Accounts model │
└────────────────┘

 Florian Dupeyron
 October 2022
"""

from enum        import Enum
from dataclasses import dataclass, field, asdict
from typing      import Optional


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
# │ Account data class                     │
# └────────────────────────────────────────┘

@dataclass
class Account:
    path: str
    name: str
    type: Account_Type
    tag:  Optional[str] = field(default=None)
