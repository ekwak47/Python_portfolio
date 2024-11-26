
def feedDog(hunger_level, biscuit_size):
    """
    Feeds Dogs using a Greedy Algorithm
    :param hunger_level:
    :param biscuit_size:
    :return:
    """
    hunger_level.sort()
    biscuit_size.sort()

    dogs_fed = 0
    x = 0
    y = 0

    while x < len(hunger_level) and y < len(biscuit_size):
        if hunger_level[x] <= biscuit_size[y]:
            dogs_fed += 1

            x += 1
            y += 1

        else:
            y += 1

    return dogs_fed
