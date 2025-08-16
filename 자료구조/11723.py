import sys

N = int(input())
input = sys.stdin.readline
bit = 0b00000000000000000000

for _ in range(N):
    b = sys.stdin.readline().rstrip().split()
    command = b[0]
    if len(b) == 2:
        num = int(b[1])-1
    if command == "add":
        bit = bit | (1 << num)
    elif command == "remove":
        bit = bit & ~(1<< num)
    elif command == "check":
        print((bit >> num) & 1)
    elif command == "toggle":
        bit = bit ^ (1 << num)
    elif command == "all":
        bit = (1 << 21) - 1
    elif command == "empty":
        bit = 0b0