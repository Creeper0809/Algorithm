import sys
from decimal import Decimal, getcontext, ROUND_HALF_UP
from tqdm import tqdm
from multiprocessing import Pool
import os

# ==============================================================================
# 1. 초기 설정 (Initialization)
# ==============================================================================

# 최대 차수(N) 설정
MAX_N = 400
# Decimal의 정밀도 설정 (충분히 높게 설정)
getcontext().prec = MAX_N * 30


# ==============================================================================
# 2. DecimalComplex 클래스 정의
# ==============================================================================

class DecimalComplex:
    """
    고정밀도(Decimal)를 지원하는 복소수 클래스
    """

    def __init__(self, real: Decimal, imag: Decimal):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        if isinstance(other, DecimalComplex):
            return DecimalComplex(self.real + other.real, self.imag + other.imag)
        raise TypeError("Unsupported operand type for +")

    def __sub__(self, other):
        if isinstance(other, DecimalComplex):
            return DecimalComplex(self.real - other.real, self.imag - other.imag)
        raise TypeError("Unsupported operand type for -")

    def __mul__(self, other):
        if isinstance(other, DecimalComplex):
            real_part = self.real * other.real - self.imag * other.imag
            imag_part = self.real * other.imag + self.imag * other.real
            return DecimalComplex(real_part, imag_part)
        raise TypeError("Unsupported operand type for *")

    def __truediv__(self, other):
        if isinstance(other, DecimalComplex):
            denom = other.real ** 2 + other.imag ** 2
            if denom == 0:
                raise ZeroDivisionError("Complex division by zero")
            real_part = (self.real * other.real + self.imag * other.imag) / denom
            imag_part = (self.imag * other.real - self.real * other.imag) / denom
            return DecimalComplex(real_part, imag_part)
        raise TypeError("Unsupported operand type for /")

    def conjugate(self):
        return DecimalComplex(self.real, -self.imag)

    def abs(self):
        return DecimalComplex((self.real ** 2 + self.imag ** 2).sqrt(), Decimal(0))

    def __repr__(self):
        sign = "+" if self.imag >= 0 else "-"
        precision_formatter = Decimal("1.00000")
        return f"({self.real.quantize(precision_formatter)} {sign} {abs(self.imag).quantize(precision_formatter)}j)"


# ==============================================================================
# 3. 사전 계산 (Pre-computation) - 이 부분은 병렬화하지 않음
# ==============================================================================

# 전역 변수로 사전 계산된 값을 저장하여 모든 자식 프로세스가 접근할 수 있도록 합니다.
print("[+] Calculating combinations (nCr)...")
Cb = [[Decimal("0") for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]
for i in range(MAX_N + 1):
    Cb[i][0] = Decimal("1")
    Cb[i][i] = Decimal("1")
    for j in range(1, i):
        Cb[i][j] = Cb[i - 1][j - 1] + Cb[i - 1][j]

EV = [[Decimal("0") for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]
DP = [[Decimal("0") for _ in range(MAX_N + 1)] for _ in range(MAX_N + 1)]
EV[0][0] = Decimal("1.0")

print("[+] Calculating EVs (E[D^p D*^q])...")
for p in tqdm(range(MAX_N + 1), desc="EV Calculation (p)"):
    for q in range(MAX_N + 1):
        if (p - q) % 6 == 0:
            if p + q > 0:
                sum_val = Decimal("0")
                for i in range(p + 1):
                    if i < p:
                        sum_val += (Cb[p][i] * DP[i][q])
                    else:
                        for j in range(q):
                            if (i - j) % 6 == 0:
                                sum_val += (Cb[p][i] * Cb[q][j]) * EV[i][j]
                denominator = Decimal(3 * (pow(2, p + q) - 1))
                if denominator != 0:
                    EV[p][q] = sum_val * Decimal(2) / denominator
        EV[q][p] = EV[p][q]

    for q_dp in range(MAX_N + 1):
        dp_sum = Decimal("0")
        for i in range(q_dp + 1):
            dp_sum += Cb[q_dp][i] * EV[p][i]
        DP[p][q_dp] = dp_sum
print("[+] EV Calculation Done!!")

print("[+] Calculating factorials and Taylor coefficients...")
factorials = [Decimal("1")]
for i in range(1, MAX_N + 1):
    factorials.append(factorials[-1] * i)

coeff = [DecimalComplex(Decimal(1), Decimal(0))]
for n in range(1, MAX_N + 1):
    fct = Decimal("1")
    for j in range(2 * n - 3, 0, -2):
        fct *= j
    c_val = Decimal(pow(-1, n + 1) * fct) / Decimal(pow(2, n) * factorials[n])
    coeff.append(DecimalComplex(c_val, Decimal(0)))
print("[+] Pre-computation finished.")


# ==============================================================================
# 4. 핵심 계산 함수 정의
# ==============================================================================

def calculate_value(U: DecimalComplex, a: DecimalComplex):
    if U.real == 0 and U.imag == 0:
        return a.abs()

    A = a / U
    B = a.conjugate() / U.conjugate()
    arrA = [DecimalComplex(Decimal(1), Decimal(0))]
    arrB = [DecimalComplex(Decimal(1), Decimal(0))]
    for i in range(1, MAX_N + 1):
        arrA.append(arrA[-1] * A)
        arrB.append(arrB[-1] * B)

    coeffA = [c * p for c, p in zip(coeff, arrA)]
    coeffB = [c * p for c, p in zip(coeff, arrB)]
    total = DecimalComplex(Decimal(0), Decimal(0))

    # 이 내부 루프는 병렬화하기 어려우므로 그대로 둡니다.
    # 대신 이 함수 자체의 호출을 병렬화합니다.
    for i in range(MAX_N + 1):
        for j in range(MAX_N + 1):
            term = coeffA[i] * coeffB[j] * DecimalComplex(EV[i][j], Decimal("0"))
            total = total + term

    total = total * U.abs()
    return total


# ==============================================================================
# 5. 병렬 처리를 위한 Worker 함수 정의
# ==============================================================================
# Pool에서 호출할 함수는 전역 수준에서 정의되어야 합니다.
# 이 함수는 각 독립적인 계산 작업을 수행합니다.
def worker(args):
    """
    하나의 (U_offset, prob) 쌍에 대한 계산을 수행하는 함수
    """
    U_offset, prob = args
    X = DecimalComplex(Decimal("0.5"), Decimal("0"))
    current_U = X + U_offset * X * X
    current_a = DecimalComplex(Decimal("0.25"), Decimal("0"))

    # tqdm을 worker 함수 내에서 사용하면 출력이 겹칠 수 있으므로,
    # 전체 진행 상황은 메인 블록에서 관리합니다.
    u = calculate_value(current_U, current_a)

    # 계산된 값에 확률을 곱하여 반환
    return u * DecimalComplex(prob, Decimal("0"))


# ==============================================================================
# 6. 메인 실행 블록 (병렬 처리 적용)
# ==============================================================================

if __name__ == "__main__":
    print("\n[+] Starting main calculation...")

    pi6 = DecimalComplex(Decimal(1) / Decimal(2), Decimal(3).sqrt() / Decimal(2))
    P6 = [DecimalComplex(Decimal(1), Decimal(0))]
    for i in range(1, 6):
        P6.append(P6[-1] * pi6)

    p1 = Decimal(1) / Decimal(3)
    p2 = Decimal(1) / Decimal(9)

    # 병렬 처리할 작업 목록 생성
    arr = [(DecimalComplex(Decimal(0), Decimal(0)), p1)]
    for i in range(6):
        if i != 3:
            arr.append((P6[i], p2))

    # --- 병렬 처리 시작 ---
    # 사용 가능한 CPU 코어 수만큼 프로세스 풀을 생성합니다.
    # os.cpu_count()는 시스템의 코어 수를 반환합니다.
    num_processes = os.cpu_count() or 1  # 코어 수를 못가져올 경우 1로 설정
    print(f"[+] Starting parallel processing on {num_processes} cores...")

    # with 구문을 사용하여 Pool을 안전하게 관리합니다.
    with Pool(processes=num_processes) as pool:
        # pool.imap을 사용하면 메모리를 효율적으로 사용하며, tqdm과 함께 진행률을 표시하기 좋습니다.
        # arr의 각 항목에 대해 worker 함수를 병렬로 실행합니다.
        results = list(tqdm(pool.imap(worker, arr), total=len(arr), desc="Main Calculation"))

    # 모든 자식 프로세스의 결과를 합산합니다.
    total_expectation = sum(results, DecimalComplex(Decimal(0), Decimal(0)))
    # --- 병렬 처리 종료 ---

    ans = total_expectation.real * Decimal("18") / Decimal("17") * Decimal("0.8")

    # --- 요청에 따른 출력 형식 수정 ---
    output_formatter = Decimal('1e-222')
    rounded_ans = ans.quantize(output_formatter, rounding=ROUND_HALF_UP)
    full_string = str(rounded_ans)
    parts = full_string.split('.')

    if len(parts) > 1:
        fractional_digits = parts[1]
    else:
        fractional_digits = '0' * 222

    # 혹시 모를 자리수 부족을 채워줍니다.
    fractional_digits = fractional_digits.ljust(222, '0')

    final_output = f"0.{fractional_digits}"

    print("\n" + "=" * 50)
    print("최종 계산 결과의 소수부를 222자리까지 반올림한 값:")
    print(final_output)
    print("=" * 50)
