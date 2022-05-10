from scompta import transactions, accounts
from pathlib import Path

df_accounts     = accounts.load_from_dir("./accounts")
df_transactions = transactions.load("transactions.csv")


print(df_accounts)
print(df_transactions)

print(transactions.undefined_accounts(df_transactions, df_accounts))

df_input        = transactions.input (df_transactions, df_accounts, "actifs/florian/ca_courant")
df_output       = transactions.output(df_transactions, df_accounts, "actifs/florian/ca_courant")

v_input         = df_input["amount"].sum()
v_output        = df_output["amount"].sum()

print("Input:  {v_input}")
print("Output: {v_output}")
