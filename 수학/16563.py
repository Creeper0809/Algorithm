import sys

input = sys.stdin.readline


def build_spf(max_n):
    spf = list(range(max_n + 1))  # 각 수에 대해 초기 최소인수는 자기 자신
    for i in range(2, int(max_n ** 0.5) + 1):
        if spf[i] == i:  # i가 소수라면
            for j in range(i * i, max_n + 1, i):
                if spf[j] == j:  # 아직 최소인수가 기록되지 않았다면
                    spf[j] = i
    return spf


def factorize(n, spf):
    factors = []
    while n != 1:
        factors.append(spf[n])
        n //= spf[n]
    return factors


def main():
    N = int(input())
    arr = list(map(int, input().split()))

    MAX_N = 5000000
    spf = build_spf(MAX_N)

    results = []
    for num in arr:
        # 소인수들을 오름차순으로 출력 (이미 SPF 방식으로 추출하면 오름차순임)
        factors = factorize(num, spf)
        results.append(" ".join(map(str, factors)))

    print("\n".join(results))


if __name__ == '__main__':
    main()
