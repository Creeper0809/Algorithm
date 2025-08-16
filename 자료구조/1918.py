n = input()

stack = list()
op_priority = {'+':1, '-':1, '*':2, '/':2,'(':-1,')':-1}
answer = list()
for i in n:
    if i not in op_priority:
        answer.append(i)
        continue

    if i == '(':
        stack.append(i)
    elif i == ')':
        while stack and stack[-1] != '(':
            answer.append(stack.pop())
        stack.pop()
    else:
        while stack and op_priority[i] <= op_priority[stack[-1]]:
            answer.append(stack.pop())
        stack.append(i)

while stack:
    answer.append(stack.pop())
print(''.join(answer))
