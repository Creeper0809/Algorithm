t = int(input())
for _ in range(t):
    n = int(input())
    melody = input()
    answer = set()
    for a in range(1,len(melody)):
        answer.add(melody[a-1:a+1])
    print(len(answer))