import logging
import pandas as pd

from scompta import accounts, transactions
from pathlib import Path

cur_dir = Path(".").resolve()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    accs = accounts.load_from_dir(cur_dir / "accounts")
    trx  = transactions.load(cur_dir / "transactions.csv")

    undef_l, undef_tr = transactions.undefined_accounts(trx, accs)

    print(accs)
    print(undef_l)
    print(undef_tr)

