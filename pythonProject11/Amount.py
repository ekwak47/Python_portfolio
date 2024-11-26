def amount(A, S):

    A.sort()

    result = []

    def backtrack(temp_list, target, start_index):

        if target == 0 and temp_list not in result:
            result.append(temp_list)
            return

        for i in range(start_index, len(A)):

            if A[i] > target:
                break

            backtrack(temp_list + [A[i]], target - A[i], i + 1)

    backtrack([], S, 0)

    return result
