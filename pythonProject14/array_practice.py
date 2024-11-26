
def list_manipulate(list):

    for i in range(len(list)):
        list[i] = list[i] + 1

    return list


list = [1, 3, 4, 5, 6, 7]
print(list_manipulate(list))


def list_replace(list, x):

    for i in range(len(list)):
        list[i] = list[x]

    return list


list = [1, 3, 4, 5, 6, 7]
print(list_replace(list, 4))


def list_mod(list):

    for i in range(len(list)):
        if list[i] >= 3:
            list[i] = list[i] // 2

        else:
            list[i] = list[i] * 3

    return list


list = [8, 1, 4, 5, 6, 7]
print(list_mod(list))


def list_cycle(list):

    for i in range(len(list) - 1):
        if list[i] > list[i + 1]:
            list[i], list[i + 1] = list[i + 1], list[i]

        else:
            list[i] = list[i + 1]

    return list


list = [8, 1, 9, 5, 6, 7]
print(list_cycle(list))


def list_sort(list):

    for i in range(len(list) - 1):
        if list[i] > list[i + 1]:
            list[i], list[i + 1] = list[i + 1], list[i]

        else:
            list[1] = list[i + 1]

    return list


list = [8, 1, 4, 90, 6, 7]
print(list_sort(list))


def array_sort(list):
    '''
    bubble sort
    :param list:
    :return:
    '''
    n = len(list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]

    return list


list = [8, 1, 4, 90, 6, 7]
print(array_sort(list))


def quicksort_arr(list, low, high):
    """Quicksort Algorithm"""
    pivot_point = list[high]
    i = low - 1

    for j in range(low, high):
        if list[j] <= pivot_point:
            i += 1
            list[i], list[j] = list[j], list[i]

    list[i + 1], list[high] = list[high], list[i + 1]

    return i + 1


def quicksort(list, low = 0, high = None):

    if high is None:
        high = len(list) - 1

    if low < high:
        pivot_index = quicksort_arr(list, low, high)
        quicksort(list, low, pivot_index - 1)
        quicksort(list, pivot_index + 1, high)

    return list


list = [8, 1, 4, 90, 6, 7, 10, 13, 12]
print(quicksort(list))
