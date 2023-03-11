"""
======================
Importer for QIF files
======================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: March 2023
"""

import logging

from money                     import Money
from scompta.model.transaction import Transaction
from pathlib                   import Path

from quiffen                   import Qif, QifDataType

log = logging.getLogger("QIF import")

def from_file(account_slug: str, fpath: Path, currency: str):
    """
    Process a QIF file into a list of transactions

    :param account_slug: Account slug
    :param fpath: Path to QIF file
    :param currency: Name of currency
    :return: A list of transactions
    """

    log.info(f"Process QIF source: {fpath}")

    fpath = Path(fpath)
    ops   = []

    # FIXME # Day first adjustement for various locales
    qif = Qif.parse(str(fpath), day_first=True)
    acc = qif.accounts["Quiffen Default Account"]

    for tr in acc.transactions["Bank"]:
        day    = tr.date.day
        amount = tr.amount
        label  = tr.payee.replace(";", " - ")

        origin = "<ORIGIN>" if amount  > 0 else account_slug
        target = "<TARGET>" if amount <= 0 else account_slug

        amount = abs(amount)

        ops.append(Transaction(
            day    = day,
            time   = "",
            label  = label,

            origin = origin,
            target = target,

            amount = Money(amount=amount, currency=currency),
            tag    = None,
        ))

    return ops

