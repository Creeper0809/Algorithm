def is_balanced(s):
    stack = []
    pairs = {')': '(', ']': '['}

    for ch in s:
        if ch in '([':
            stack.append(ch)
        elif ch in ')]':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack

while True:
    line = input()
    if line == ".":
        break
    print("yes" if is_balanced(line) else "no")
