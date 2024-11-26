def powerset(inputSet):
    """
    Returns power set of
    :param inputSet:
    :return:
    """
    if inputSet == []:
        return [[]]

    results = powerset_helper(len(inputSet) - 1, [], inputSet, [])
    return results


def powerset_helper(pointer, subset, inputSet, result):
    """
    helper function which gets our powerset
    """
    if pointer < 0:
        return result.append(subset[::-1])

    subset.append(inputSet[pointer])
    powerset_helper(pointer - 1, subset, inputSet, result)
    subset.pop()
    powerset_helper(pointer - 1, subset, inputSet, result)
    return result
