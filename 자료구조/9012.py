T = int(input())
def is_perfect(words):
    stack = []
    for word in arr:
        if word == "(":
            stack.append(word)
        elif word == ")":
            if not stack:
                return False
            stack.pop()
    return not stack

for _ in range(T):
    arr = input()
    if is_perfect(arr):
        print("YES")
    else:
        print("NO")

