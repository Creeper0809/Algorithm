import math

if __name__ == '__main__':
    N = int(input())
    factorialN = str(math.factorial(N))
    count = 0
    for i in factorialN[::-1]:
        if int(i) != 0:
            break
        count+=1
    print(count)

