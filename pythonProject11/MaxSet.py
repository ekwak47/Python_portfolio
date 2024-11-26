def max_independent_set(nums):
    """
    Takes an array of numbers and returns a set of non-consecutive integers for the
    maximum possible sum
    :param nums:
    :return:
    """
    if nums is None:
        return []

    if all(num < 0 for num in nums):
        return []

    num = len(nums)
    dp = [0] * (num + 1)
    dp[1] = nums[0]
    sum_nums = []

    for i in range(2, (num + 1)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1], nums[i - 1])

    while num > 0:
        if dp[num] >= 0:
            if dp[num] == dp[num - 1]:
                num -= 1
            else:
                sum_nums.append(nums[num - 1])
                num -= 2
        else:
            num -= 1

    return sum_nums[::-1]
