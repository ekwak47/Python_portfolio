def dna_match_topdown(DNA1, DNA2):
    dnamemo = dict()
    return dnafunc(DNA1, DNA2, len(DNA1), len(DNA2), dnamemo)


def dnafunc(DNA1, DNA2, m, n, dnamemo):
    """helper function that helps the topdown approach"""
    if (m, n) in dnamemo:
        return dnamemo[(m, n)]
    if m == 0 or n == 0:
        dnamemo[(m, n)] = 0
        return dnamemo[(m, n)]
    elif DNA1[m - 1] == DNA2[n - 1]:
        dnamemo[(m, n)] = 1 + dnafunc(DNA1, DNA2, m - 1, n - 1, dnamemo)
        return dnamemo[(m, n)]
    else:
        dnamemo[(m, n)] = max(dnafunc(DNA1, DNA2, m, n - 1, dnamemo), dnafunc(DNA1, DNA2, m - 1, n, dnamemo))
        return dnamemo[(m, n)]


def dna_match_bottomup(DNA1, DNA2):
    """Bottonup implementation for DNAmatch"""
    m = len(DNA1)
    n = len(DNA2)

    dna_table = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    """initializes table to store values"""

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i == 0 or j == 0:
                dna_table[i][j] = 0
            elif DNA1[i - 1] == DNA2[j - 1]:
                dna_table[i][j] = dna_table[i - 1][j - 1] + 1
            else:
                dna_table[i][j] = max(dna_table[i - 1][j], dna_table[i][j - 1])

    return dna_table[m][n]
