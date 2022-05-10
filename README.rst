=============================================
SympaCompta: Personnal accounting made easier
=============================================

:Authors:   - Florian Dupeyron <florian.dupeyron@mugcat.fr>

What is this ?
==============

SympaCompta is a python toolkit aiming at simplfying your personnal accounting workflow by
packing easy-to-use tools as python modules. You can build custom scripts and interfaces on top
of that, for example to manage transactions, generate various reports, or integrate data from
other sources (stock markets for instance).

Dependecies
===========

- pandas
- numpy
- money (the package, not the actual thing)

Key concepts
============

Accounts and transactions
-------------------------

Accounts
~~~~~~~~

This toolkit implements a double-entry like bookkeeping system, inspired by Gnucash_. This means:

- Everything is an account (no category system) ;
- For every transaction, there is a source account, and a destination account. For instance, your checking account, to the account representing your rent.

There are currently four major types of accounts:

- Assets
- Liabilities
- Income
- Outcome

No Equity type is currently implemented. The equity can be checked by user scripts.

Let's take some basic examples:

- Your checking account is an asset account ;
- Your rent account is an outcome account ;
- Your salary account is an income account ;
- Your loan account is a liability account.

The key to understand the double entry system is to remember the following equation:

.. math::

   equity - outcome = assets - liability + income


.. _Gnucash: TODO

Transactions
~~~~~~~~~~~~

Transactions have the following information:

- The day of the transaction;
- An optional time;
- The source account;
- The destination account;
- The amount;
- An optional tag

As this toolkit is intended for personal accounting, a canonical period of **1 month** is defined to group the transactions. This is why
only the day is stored.

Recommended folder hierarchy
----------------------------

The recommended folder hierarchy is the following:

.. code::

    root_folder
    ├── accounts
    │   ├── assets
    │   │   ├── common
    │   │   │   └── checking.toml
    │   │   ├── person1
    │   │   │   ├── cash.toml
    │   │   │   └── checking.toml
    │   │   └── person2
    │   │       ├── cash.toml
    │   │       └── checking.toml
    │   ├── income
    │   │   ├── person1
    │   │   │   └── salary.toml
    │   │   └── person2
    │   │       └── salary.toml
    │   ├── liabilities
    │   │   └── common
    │   │       └── house_loan.toml
    │   └── outcome
    │       ├── common
    │       │   └── household
    │       │       ├── food.toml
    │       │       ├── internet.toml
    │       │       ├── rent.toml
    │       │       └── tv.toml
    │       ├── person1
    │       │   ├── food.toml
    │       │   └── phone.toml
    │       └── person2
    │           ├── food.toml
    │           └── phone.toml
    ├── periods
    │   ├── 2022-01
    │   │   └── transactions.csv
    │   ├── 2022-02
    │   │   └── transactions.csv
    │   ├── 2022-03
    │   │   └── transactions.csv
    │   ├── 2022-04
    │   │   └── transactions.csv
    │   └── 2022-05
    │       └── transactions.csv
    └── reports
        ├── report1.py
        └── report2.py

As all used files are text based, it should be well suited to be used with version control software, like git!

Recommended format for transactions
-----------------------------------

Transactions for 1 period (= 1 month) are stored in a CSV file. For example:

.. code:: csv
    
    day;time;label;from;to;amount;tag
    2;;Salary may;income/person1/salary;assets/person1/checking;EUR 1000.000;salary
    3;;Rent may;assets/person1/checking;outcome/common/household/loan;EUR 300.0;rent
    5;12:00;Lunch;assets/person1/checking;outcome/person1/food;10.00;

**Please note**:

- Accounts are identified by their relative path from the accounts folder, without the extension ;
- Currency information is given in the amount field ;
- This specific header is mandatory.

As the CSV format is pretty common, you can use your favorite tool to edit it. For instance, if you
want easy remote editing, you could use google sheets (untested at this point).

Recommended format for accounts description
-------------------------------------------

The recommended format to describe an account in a `toml` file is the following:

.. code:: toml

    [account]
    name="Checking acount for Person1"
    type="assets"

At this moment, only these two fields are mandatory and available.

Example report script
=====================

The purpose of the following script is to compute the final balance of all the assets, and to
fix the amounts to save in various accounts:

.. code:: python

    import argparse
    import logging

    from pathlib import Path
    from scompta import accounts, transactions
    from decimal import Decimal

    # Helper to parse directories
    def __parse_dir(x):
    dpath = Path(x)
    if not dpath.is_dir():
        raise NotADirectoryError(x)
    else:
        return dpath

    # Root directory
    root_dir = (Path(__file__).parent / "..").resolve()

    # Parse arguments
    parser = argparse.ArgumentParser(description="Report saving strategy for the given period")
    parser.add_argument("folder", type=__parse_dir)

    args = parser.parse_args()

    # Load accounts
    df_accs         = accounts.load_from_dir(root_dir / "accounts")
    df_transactions = transactions.load(args.folder / "transactions.csv")

    # Find assets accounts
    df_accs_assets  = accounts.with_type(accounts.Account_Type.Assets)

    # Find gain and losses transactions
    t_in  = transactions.input (df_transactions, df_accs, df_accs_assets.index)
    t_out = transactions.output(df_transactions, df_accs, df_accs_assets.index)

    # Compute total gains and losses, and final balance
    v_in  = t_in["amount"].sum()
    v_out = t_out["amount"].sum()
    v_bal = v_in - v_out

    # Print stuff
    print()
    print("# ──────────────── Amounts ─────────────── #")
    print()
    print(f"Gains:                 {v_in}")
    print(f"Losses:                {v_out}")
    print(f"Available for savings: {v_bal}")
    print()
    print("# ──────────────── Savings ─────────────── #")
    print()

    v_savings_1 = v_bal*Decimal(0.2) # 20% for one account
    v_savings_2 = v_bal*Decimal(0.5) # 50% for another account
    v_savings_3 = v_bal*Decimal(0.1) # 10% for this one
    v_savings_4 = v_bal*Decimal(0.2) # 20% for this one

    print(f"Account 1: {v_savings_1}")
    print(f"Account 2: {v_savings_2}")
    print(f"Account 3: {v_savings_3}")
    print(f"Account 4: {v_savings_4}")
