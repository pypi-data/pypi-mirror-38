from decimal import Decimal
from . import utils


# add inputs until we reach or surpass the target value (or deplete)
# worst-case: O(n)
def accumulative(utxos, outputs, feeRate):
    feeRate = Decimal(feeRate)
    bytesAccum = utils.transactionBytes([], outputs)

    inAccum = 0
    inputs = []
    outAccum = utils.sumOrNaN(outputs)
    for i in range(len(utxos)):
        utxo = utxos[i]
        utxoBytes = utils.inputBytes(utxo)
        utxoFee = feeRate * utxoBytes
        utxoValue = Decimal(utxo['value'])

        # skip detrimental input
        if utxoFee >= utxoValue:
            if (i == len(utxos) - 1):
                return {'fee': round(feeRate * (bytesAccum + utxoBytes))}
            continue
        bytesAccum += utxoBytes
        inAccum += utxoValue
        inputs.append(utxo)
        fee = feeRate * bytesAccum

        # go again?
        if inAccum < outAccum + fee:
            continue

        return utils.finalize(inputs, outputs, feeRate)

    return {'fee': round(feeRate * bytesAccum)}
