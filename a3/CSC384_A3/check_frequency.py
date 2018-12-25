def check_pivot(l, frequency):
    """
    l is list of 0 and 1
    len(l) >= frequency
    """
    # find the index of the first 1
    pivot = len(l)
    for i in range(len(l)):
        if l[i] == 1:
            pivot = i
            break
    if pivot >= frequency:
        return False
    while pivot < len(l) - 3:
        flag = 0
        for i in range(pivot+1, pivot+4):
            if l[i] == 1:
                flag = 1
                pivot = i
        if flag == 0:
            return False
    return True


if __name__ == '__main__':
    print(check_pivot([0, 0, 1], 3))    # true
    print(check_pivot([0, 0, 0], 3))    # false
    print(check_pivot([0, 0, 0, 1], 3)) # false
    print(check_pivot([0, 1, 0, 1], 3)) # true
    print(check_pivot([0, 1, 0, 0, 0, 1], 3))  # false
    print(check_pivot([0, 1, 0, 0, 1, 0, 0], 3))  # true
    print(check_pivot([0, 1, 0, 0, 1, 0, 0, 0], 3))  # false
    print(check_pivot([1, 1], 2))  # t
    print(check_pivot([1, 1, 1, 1], 2))  # t
