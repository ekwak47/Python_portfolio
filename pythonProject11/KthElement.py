
def kthElement(arr1, arr2, k):
    """
    Takes two sorted arrays and finds kth position in combined sorted array
    :param arr1:
    :param arr2:
    :param k:
    :return:
    """
    # base case for empty arrays
    if len(arr1) == 0:
        return arr2[k - 1]
    if len(arr2) == 0:
        return arr1[k - 1]
    if k == 1:
        return min(arr1[0], arr2[0])
    # cuts both arrays in half
    cut1 = len(arr1) // 2
    cut2 = len(arr2) // 2
    # if one of the sliced arrays are less than or equal to
    if arr1[cut1 - 1] <= arr2[cut2 - 1]:
        if k < cut1 + cut2 + 1:
            return kthElement(arr1, arr2[1:cut2 + 1], k)
        else:
            return kthElement(arr1[cut1 + 1:], arr2, k - cut1 - 1)
    else:
        if k < cut1 + cut2 + 1:
            return kthElement(arr1[1:cut1 + 1], arr2, k)
        else:
            return kthElement(arr1, arr2[cut2 + 1:], k - cut2 - 1)
       