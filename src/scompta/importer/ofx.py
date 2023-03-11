"""
======================
Importer for OFX files
======================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: March 2023
"""

import logging

from money                     import Money # Gotta get rich!
from scompta.model.transaction import Transaction
from pathlib                   import Path

from ofxtools.Parser           import OFXTree

log = logging.getLogger("OFX import")

def from_file(account_slug: str, fpath: Path):
    """
    Process an OFX file into a list of transactions
    
    :param account_slug: Account slug
    :param fpath: Path to OFX file
    :return: A list of transactions
    """

    log.info(f"Process OFX file: {fpath} for {account_slug}")

    fpath = Path(fpath)
    ops   = []

    parser = OFXTree()
    parser.parse(str(fpath))
    ofx = parser.convert()

    currency     = ofx.statements[0].curdef
    transactions = ofx.statements[0].transactions

    
    for tr in transactions:
        dtposted = tr.dtposted
        amount   = tr.trnamt
        memo     = (tr.memo or tr.name).replace(";", " - ")

        origin   = "<ORIGIN>" if amount  > 0 else account_slug
        target   = "<TARGET>" if amount <= 0 else account_slug

        amount   = abs(amount)

        ops.append(Transaction(
            day    = dtposted.day,
            time   = "",
            label  = memo,
            origin = origin,
            target = target,

            amount = Money(amount=amount, currency=currency),
            tag    = None,
        ))

    return ops
