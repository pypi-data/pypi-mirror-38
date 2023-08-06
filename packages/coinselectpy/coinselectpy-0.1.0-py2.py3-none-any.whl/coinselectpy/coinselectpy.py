# -*- coding: utf-8 -*-

"""Main module."""

from .accumulative import accumulative
from .blackjack import blackjack
from . import utils
from decimal import Decimal


def coinSelect(utxos, outputs, feeRate):
    feeRate = Decimal(feeRate)

    # order by descending value, minus the inputs approximate fee
    def utxoScore(x, fr):
        return round(x.get('value', 0) - (fr * utils.inputBytes(x)))

    utxos.sort(key=lambda x: utxoScore(x, feeRate), reverse=True)
    print(utxos)

    base = blackjack(utxos, outputs, feeRate)
    if base.get('inputs', []):
        return base

    return accumulative(utxos, outputs, feeRate)
