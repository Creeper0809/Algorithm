def hanoi(num, start, middle, end):
    if num == 1:
        print(start, end)
    else:
        hanoi(num - 1, start, end, middle)
        print(start, end)
        hanoi(num - 1, middle, start, end)


num = int(input())
print((2 ** num) - 1)
if num < 21:
    hanoi(num, 1, 2, 3)
