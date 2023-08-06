from decimal import Decimal
from . import utils


# only add inputs if they don't bust the target value (aka, exact match)
# worst-case: O(n)
def blackjack(utxos, outputs, feeRate):
    feeRate = Decimal(feeRate)
    bytesAccum = utils.transactionBytes([], outputs)

    inAccum = 0
    inputs = []
    outAccum = utils.sumOrNaN(outputs)
    threshold = utils.dustThreshold({}, feeRate)

    for i in range(len(utxos)):
        input = utxos[i]
        inputBytes = utils.inputBytes(input)
        fee = feeRate * (bytesAccum + inputBytes)
        inputValue = Decimal(input['value'])

        # would it waste value?
        if ((inAccum + inputValue) > (outAccum + fee + threshold)):
            continue

        bytesAccum += inputBytes
        inAccum += inputValue
        inputs.append(input)

        # go again?
        if inAccum < outAccum + fee:
            continue

        return utils.finalize(inputs, outputs, feeRate)

    return {'fee': round(feeRate * bytesAccum)}
