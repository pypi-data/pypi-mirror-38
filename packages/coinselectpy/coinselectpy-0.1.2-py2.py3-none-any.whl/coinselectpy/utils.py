from functools import reduce
from decimal import Decimal

# baseline estimates, used to improve performance
TX_EMPTY_SIZE = 4 + 1 + 1 + 4
TX_INPUT_BASE = 32 + 4 + 1 + 4 + 1
TX_INPUT_PUBKEYHASH = 106
TX_OUTPUT_BASE = 8 + 1
TX_OUTPUT_PUBKEYHASH = 25


def inputBytes(input):
    return TX_INPUT_BASE + \
        (len(input.get('script', ''))
            if input.get('script', '')
            else TX_INPUT_PUBKEYHASH)


def outputBytes(output):
    return TX_OUTPUT_BASE + \
        (len(output.get('script', ''))
            if output.get('script', '')
            else TX_OUTPUT_PUBKEYHASH)


def dustThreshold(output, feeRate):
    # classify the output for input estimate
    return round(inputBytes({}) * feeRate)


def transactionBytes(inputs, outputs):
    return TX_EMPTY_SIZE\
        + reduce(lambda a, x: a + inputBytes(x), inputs, 0)\
        + reduce(lambda a, x: a + outputBytes(x), outputs, 0)


def sumForgiving(dict_list):
    return reduce(lambda a, x: a + int(x.get('value', 0)), dict_list, 0)


def sumOrNaN(dict_list):
    return reduce(lambda a, x: a + int(x.get('value', 0)), dict_list, 0)


BLANK_OUTPUT = outputBytes({})


# feeRate: satochi per byte
def finalize(inputs, outputs, feeRate):
    feeRate = Decimal(feeRate)
    bytesAccum = transactionBytes(inputs, outputs)
    feeAfterExtraOutput = round(feeRate * (bytesAccum + BLANK_OUTPUT))
    remainderAfterExtraOutput = \
        sumOrNaN(inputs) - (sumOrNaN(outputs) + feeAfterExtraOutput)

    # is it worth a change output?
    if remainderAfterExtraOutput > dustThreshold({}, feeRate):
        outputs.append({'value': remainderAfterExtraOutput})

    fee = sumOrNaN(inputs) - sumOrNaN(outputs)

    return {
        'inputs': inputs,
        'outputs': outputs,
        'fee': fee,
    }
