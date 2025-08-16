#!/usr/bin/env python3
import random, re
from pwn import remote, log

HOST, PORT = 'host3.dreamhack.games', 23069
CONST = 0xDEADDEADBEEFBEEFCAFECAFE13371337DEFACED0DEFACED0
CHAL_RX = re.compile(rb'"(\d+)"')  # bytes 패턴

def split_six(dec_str: str):
    """10진수 문자열 → 6개 32-bit word 리스트"""
    v = int(dec_str)
    r = v ^ CONST
    return [(r >> (32 * i)) & 0xFFFFFFFF for i in range(6)]

def untemper(y: int) -> int:
    """Mersenne-Twister 텀퍼링 역변환"""
    y ^= y >> 18
    y ^= (y << 15) & 0xEFC60000
    for _ in range(4):
        y ^= (y << 7) & 0x9D2C5680
    y ^= y >> 11
    y ^= y >> 11
    return y & 0xFFFFFFFF

def build_state(words):
    """624개 word → random.setstate()용 tuple 생성"""
    assert len(words) >= 624, "MT 상태 복구하려면 624개 word가 필요합니다."
    mt = tuple(untemper(w) for w in words[:624])
    return (3, tuple(mt + (624,)), None)

def next_challenge(rng: random.Random) -> int:
    vals = [rng.randint(0, 0xFFFFFFFE) for _ in range(6)]
    r224 = sum(v << (32 * i) for i, v in enumerate(vals))
    return r224 ^ CONST

def main():
    p  = remote(HOST, PORT)
    ws = []   # 32-bit word 저장용

    # ─── 1) 최초 624 word 수집 ────────────────────
    while len(ws) < 624:
        p.sendlineafter(b'> ', b'2')            # (A) verify 호출
        line = p.recvline()                     # (B) challenge₁ 줄 수신
        chal_b = CHAL_RX.findall(line)[0]       # b'xxxxx...' (bytes)
        print(f'[CHAL] {chal_b.decode()}')       # 디버깅 출력

        # (C) 틀려도 상관 없지만, 그냥 제대로 echo → 서버가 실패 판단
        p.sendline(b"asd")
        p.recvuntil(b'> ')                      # (D) "you’re not a robot ;[ + 메뉴"까지 흡수

        ws.extend(split_six(chal_b.decode()))   # (E) 6개 word 저장

    # ─── 2) MT 상태 복구 ─────────────────────────
    rng = random.Random()
    rng.setstate(build_state(ws))
    log.success('MT 상태 복구 완료!')

    # ─── 3) “예측 → 검증” 단계 ────────────────────
    ## (F) 다시 verify₁ 호출
    p.sendline(b'2')
    line = p.recvline()
    chal_b1 = CHAL_RX.findall(line)  # 서버가 내보낸 verify₁의 challenge₁
    log.info(f'verify₁ 실제 challenge₁: {chal_b1}')

    ## (G) 예측값 계산
    pred = str(next_challenge(rng)).encode()
    log.info(f'계산된 예측값       : {pred.decode()}')

    ## (H) pred를 echo
    p.sendline(pred)
    p.recvuntil(b'> ')     # “verified” 또는 “you’re not a robot ;[” + 다음 메뉴 프롬프트까지 흡수

    ## (I) 이제 내부 index가 624 + 6 = 630. verify₂ 시 challenge₂가 pred가 되어야 한다
    p.sendline(b'2')
    line2 = p.recvline()
    chal_b2 = CHAL_RX.findall(line2)
    log.info(f'verify₂ 실제 challenge₂: {chal_b2}')

    if chal_b2 == pred:
        log.success('예측 성공! 🎯')
    else:
        log.error('예측 실패… 인덱스가 어긋났습니다.')

    # ─── 4) 이후 원한다면 3. buy flag 선택 등 계속 진행… ──
    p.interactive()


if __name__ == '__main__':
    main()
