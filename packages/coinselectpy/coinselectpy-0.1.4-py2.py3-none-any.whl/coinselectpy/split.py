from functools import reduce
from decimal import Decimal
from . import utils
import math


def split(utxos, outputs, feeRate):
    feeRate = Decimal(feeRate)

    bytesAccum = utils.transactionBytes(utxos, outputs)
    fee = round(feeRate * bytesAccum)
    if not outputs:
        return {'fee': fee}

    inAccum = utils.sumOrNaN(utxos)
    outAccum = utils.sumForgiving(outputs)
    remaining = inAccum - outAccum - fee
    if remaining < 0:
        return {'fee': fee}
    elif remaining == 0:
        return utils.finalize(utxos, outputs, feeRate)

    splitOutputsCount = reduce(
        lambda a, x: a + (1 if 'value' not in x else 0),
        outputs,
        0)
    splitValue = math.floor(remaining / splitOutputsCount)

    # ensure every output is either user defined, or over the threshold
    if any([x for x in outputs
            if utils.dustThreshold(x, feeRate) >= splitValue]):
        return {'fee': fee}

    # assign splitValue to outputs not user defined
    outputs = [x if 'value' in x else dict(value=splitValue, **x)
               for x in outputs]

    return utils.finalize(utxos, outputs, feeRate)
