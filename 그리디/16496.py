from functools import cmp_to_key
N = int(input())
arr = list(map(str,input().split()))

def compare(x,y):
    if x + y < y + x:
        return 1
    return -1


arr.sort(key=cmp_to_key(compare))
print(int("".join(arr)))