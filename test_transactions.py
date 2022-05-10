import numpy  as np
import pandas as pd

from scompta import transactions, accounts

################################

account_name="actifs/florian/ca_courant"

df          = transactions.load("transactions.csv")
df_accounts = accounts.load_from_dir("./accounts")

print(df)

v_in    = transactions.input (df, df_accounts, account_name)
v_out   = transactions.output(df, df_accounts, account_name)

print(f"Input   for {account_name}: ", v_in ["amount"].sum())
print(f"Output  for {account_name}: ", v_out["amount"].sum())
print(f"Balance for {account_name}: ", v_in["amount"].sum() - v_out["amount"].sum())

# Find outcome for food stuff
df_food = df.loc[df["to"] == "depenses/commun/vie_quotidienne/alimentaire"]
