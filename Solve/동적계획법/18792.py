import sys
from itertools import combinations
import bisect


# 왼쪽 혹은 오른쪽 부분에 대해, 모든 부분집합 후보를 생성하는 함수
# arr: 부분 배열, offset: 원래 배열에서의 시작 인덱스 (출력 시 원래 인덱스로 복원하기 위해)
# N: 전체 문제에서 필요한 모듈로(또는 N, 여기서는 N으로 mod 연산을 함)
def gen_subsets(arr, offset, N):
    candidates = []  # 각 후보는 (count, mod, subset) 형태. subset은 원래 배열의 인덱스 튜플.
    m = len(arr)
    for cnt in range(m + 1):  # cnt: 선택할 원소 개수 (0부터 m까지)
        for comb in combinations(range(m), cnt):
            # comb는 arr내의 인덱스들; 원래 인덱스는 각에 offset을 더한 값
            subset = tuple(i + offset for i in comb)
            total = sum(arr[i] for i in comb)
            mod_val = total % N
            candidates.append((cnt, mod_val, subset))
    return candidates


def solve():
    input = sys.stdin.readline
    N = int(input())
    nums = list(map(int, input().split()))
    M = len(nums)  # 문제 조건에 따르면 보통 2N - 1개

    # 절반으로 분할 (왼쪽, 오른쪽)
    half = M // 2
    left_arr = nums[:half]
    right_arr = nums[half:]

    # 왼쪽과 오른쪽 후보 생성.
    left_candidates = gen_subsets(left_arr, 0, N)
    right_candidates = gen_subsets(right_arr, half, N)

    # 오른쪽 후보들을 (count, mod, subset) 기준으로 정렬
    right_candidates.sort(key=lambda x: (x[0], x[1], x[2]))

    # 이분탐색을 위한 키 생성 함수.
    # 오른쪽 후보에서, (count, mod, ...)가 target와 일치하는 위치를 찾는다.
    def candidate_key(candidate):
        return (candidate[0], candidate[1])

    # 오른쪽 후보 리스트에서 특정 (req_count, req_mod) 조건을 만족하는 후보가 있는지 이분탐색
    # 리턴 값은 후보 튜플 또는 None.
    def find_candidate(req_count, req_mod):
        # 우리가 찾고자 하는 키의 최소값: (req_count, req_mod, empty tuple)
        target = (req_count, req_mod, ())
        i = bisect.bisect_left(right_candidates, target, key=lambda x: (x[0], x[1], x[2]))
        if i < len(right_candidates):
            cand = right_candidates[i]
            if cand[0] == req_count and cand[1] == req_mod:
                return cand
        return None

    # 왼쪽 후보들을 순회하면서, 만약 왼쪽에서 cnt_left개 뽑았고 합의 mod값이 mod_left라면,
    # 오른쪽에서는 나머지 개수 req_count = N - cnt_left가 필요하며,
    # 그 오른쪽 후보의 mod값은 ( - mod_left mod N )여야 함.
    for cnt_left, mod_left, left_subset in left_candidates:
        req_count = N - cnt_left
        req_mod = (-mod_left) % N
        # 이분탐색을 통해 오른쪽에서 조건을 만족하는 후보를 찾는다.
        cand = find_candidate(req_count, req_mod)
        if cand is not None:
            _, _, right_subset = cand
            # 왼쪽과 오른쪽에서 선택된 인덱스를 합치기
            full_subset = left_subset + right_subset
            # full_subset은 원래 배열 nums의 인덱스 (순서는 오름차순이 아니어도 됨)
            # 결과 출력: 해당 인덱스에 해당하는 원소들을 출력
            result = [nums[i] for i in sorted(full_subset)]
            print(" ".join(map(str, result)))
            return

    print(-1)


if __name__ == "__main__":
    solve()
