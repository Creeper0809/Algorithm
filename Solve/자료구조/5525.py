from collections import deque

N = int(input())
M = int(input())
string = input()


answer = 0
pattern = 0
i = 0
while i< M-2:
    if string[i] == "I" and string[i+1] == "O" and string[i+2] == "I":
        pattern += 1
        if pattern == N:
            pattern -= 1
            answer += 1
        i += 2
    else:
        i += 1
        pattern = 0
print(answer)
