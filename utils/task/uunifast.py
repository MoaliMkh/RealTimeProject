import random


def uunifast(n, utilization):
    utilizations = []
    sumU = utilization
    for i in range(1, n):
        nextSumU = sumU * random.uniform(0, 1) ** (1 / (n - i))
        utilizations.append(sumU - nextSumU)
        sumU = nextSumU
    utilizations.append(sumU)

    return utilizations
