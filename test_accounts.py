import logging
import pandas as pd

from scompta import accounts
from pathlib import Path

cur_dir = Path(".").resolve()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    accs = accounts.load_from_dir(cur_dir / "accounts")

    print(accs.loc[accs["type"] == accounts.Account_Type.Income])
