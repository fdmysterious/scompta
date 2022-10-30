from scompta import transactions, accounts
from pathlib import Path

import scompta.db.accounts     as accounts_db
import scompta.db.transactions as transactions_db

from   scompta.views import transactions as transactions_views

df_accounts     = accounts_db.load_from_dir("./accounts")
df_transactions = transactions_db.load("transactions.csv")

print(df_accounts)
print(df_transactions)

print(transactions_views.undefined_accounts(df_transactions, df_accounts))

df_input        = transactions_views.input (df_transactions, df_accounts, "actifs/florian/ca_courant")
df_output       = transactions_views.output(df_transactions, df_accounts, "actifs/florian/ca_courant")

v_input         = df_input["amount"].sum()
v_output        = df_output["amount"].sum()

print(f"Input:  {v_input}")
print(f"Output: {v_output}")
