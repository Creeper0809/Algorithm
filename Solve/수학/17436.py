#포함배제원리의 이해를 위해 챗gpt와 함께 했다
from math import lcm

# 위의 코드를 포함배제 원리를 이용하여 구현하면 다음과 같다.
def get_prime_divisible_count(primes, n):
    count = 0  # 나누어 떨어지는 수의 개수를 저장할 변수 count를 0으로 초기화
    for i in range(1, 2**len(primes)):  # 1부터 2^len(primes)까지 반복문 수행
        print(i)
        s = set()  # i에 대응하는 집합 s를 구성하기 위해 set() 함수를 사용하여 빈 집합 생성
        for j in range(len(primes)):  # primes 리스트의 인덱스를 하나씩 가져와서 반복문 수행
            if i & (1 << j):  # i의 j번째 비트가 1인 경우
                s.add(primes[j])  # 해당 소수를 집합 s에 추가
        sign = -1 if len(s) % 2 == 0 else 1  # 집합의 부호 결정
        count += sign * (n // lcm(*s))  # 최종 결과에 계산된 값 더하기 또는 빼기
    return count  # count 값을 반환


n,m = list(map(int,input().split()))
prime = list(map(int,input().split()))

#print(get_prime_divisible_count(prime, m))  # 함수를 호출하여 결과 출력

a = set()

for i in prime:
    for j in range(i,m+1,i):
        a.add(j)
print(a)