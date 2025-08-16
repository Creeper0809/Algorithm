import sys

input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    # depth 계산
    T = 0
    for ai in a:
        if ai != -1 and ai > T:
            T = ai
    depth = [(T + 1 if ai == -1 else ai) for ai in a]

    # 결과 순열
    p = [0] * n
    # 다음 할당에 쓸 작은값(low)·큰값(high) 포인터
    low, high = 1, n
    # 현재 iteration 에 살아남은 인덱스들(처음엔 0..n-1)
    order = list(range(n))

    for k in range(1, T + 1):
        segs = []  # 제거될 인덱스들을 세그먼트 단위로
        curr = []
        survivors = []  # depth>k 인 인덱스들

        # order 를 스캔하며 depth==k 인 것들은 curr 에 모으고
        # depth>k 인 것들은 survivors 로 분기
        for i in order:
            if depth[i] == k:
                curr.append(i)
            else:
                if curr:
                    segs.append(curr)
                    curr = []
                survivors.append(i)
        if curr:
            segs.append(curr)

        removed_count = sum(len(seg) for seg in segs)

        # suffix 세그먼트 판별 (마지막 살아남은 위치 이후에 나오는 세그먼트)
        if survivors:
            last_surv = survivors[-1]
            if segs and segs[-1][0] > last_surv:
                suffix = segs[-1]
                prefix_segs = segs[:-1]
            else:
                suffix = []
                prefix_segs = segs
        else:
            # k<T 에는 반드시 survivors 가 있으므로 여기엔 안 걸림
            suffix = []
            prefix_segs = segs

        # 값 할당: 홀수(iteration=1,3,5..)인 경우 local-min 삭제 → 큰 값을 줘서 제거
        if k & 1:
            hi_init = high
            lo_end = hi_init - removed_count + 1
            cur_hi = hi_init
            # prefix·interior 세그먼트: 큰 값부터
            for seg in prefix_segs:
                for i in seg:
                    p[i] = cur_hi
                    cur_hi -= 1
            # suffix 세그먼트: 작은 값부터
            for idx, i in enumerate(suffix):
                p[i] = lo_end + idx
            high = lo_end - 1
        else:
            # 짝수(iteration=2,4..)인 경우 local-max 삭제 → 작은 값을 줘서 제거
            lo_init = low
            hi_end = lo_init + removed_count - 1
            cur_lo = lo_init
            # prefix·interior 세그먼트: 작은 값부터
            for seg in prefix_segs:
                for i in seg:
                    p[i] = cur_lo
                    cur_lo += 1
            # suffix 세그먼트: 큰 값부터 내림차순
            for idx, i in enumerate(suffix):
                p[i] = hi_end - idx
            low = hi_end + 1

        # 다음 iteration 을 위해 survivors 만 남김
        order = survivors

    # 마지막 살아남은 위치(depth=T+1)들에 남은 값 할당
    for i in order:
        p[i] = low
        low += 1

    print(*p)
