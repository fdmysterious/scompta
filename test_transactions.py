import numpy  as np
import pandas as pd

from scompta import transactions

################################

df = transactions.load("transactions.csv")

v_in    = transactions.input(df, "ca_courant")
v_out   = transactions.output(df, "ca_courant")

print(df)
print("Input   for ca_courant: ", v_in ["amount"].sum())
print("Output  for ca_courant: ", v_out["amount"].sum())
print("Balance for ca_courant: ", v_in["amount"].sum() - v_out["amount"].sum())
