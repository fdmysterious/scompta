import numpy  as np
import pandas as pd

from scompta import transactions

################################

account_name="actifs/florian/ca_courant"

df = transactions.load("transactions.csv")

print(df)

v_in    = transactions.input (df, account_name)
v_out   = transactions.output(df, account_name)

print(f"Input   for {account_name}: ", v_in ["amount"].sum())
print(f"Output  for {account_name}: ", v_out["amount"].sum())
print(f"Balance for {account_name}: ", v_in["amount"].sum() - v_out["amount"].sum())
