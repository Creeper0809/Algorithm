def count_digit_occurrences(N):
    result = [0] * 10
    multiplier = 0
    original_N = N

    while N > 0:
        digit = N % 10
        power = 10 ** multiplier
        left = N // 10
        right = original_N % power

        # 현재 자릿수보다 높은 자리수로 인해 반복된 횟수
        for i in range(10):
            result[i] += left * power

        # 현재 자릿수의 digit보다 작은 숫자들은 1세트 더 등장
        for i in range(digit):
            result[i] += power

        # 현재 자릿수의 숫자 그 자체는 하위 숫자(right)만큼 추가 등장
        result[digit] += right + 1

        # 앞자리 0 보정 (0은 숫자의 맨 앞에 올 수 없으므로 빼줌)
        if multiplier > 0:
            result[0] -= power

        multiplier += 1
        N //= 10

    return result

N = int(input())
result = count_digit_occurrences(N)
result[0] -= 1
print(*result)
