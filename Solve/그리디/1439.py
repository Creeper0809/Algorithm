if __name__ == '__main__':
    S = input()
    before = ""
    count = 0
    for i in S:
        if i == before:
            continue
        before = i
        count += 1
    if count == 1:
        print(0)
    else:
        print(int(count / 2))