N = int(input())

result = 0

def back_tracking(count):
    global result
    if count == N:
        result += 1
        return
    for i in range(N):
        graph[count] = i
        if is_vailid(count):
            back_tracking(count + 1)

def is_vailid(count):
    for i in range(count):
        if graph[i] == graph[count] or count - i == abs(graph[count] - graph[i]):
            return False
    return True

graph = [-1] * N
back_tracking(0)
print(result)