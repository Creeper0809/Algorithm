# 주어진 hex 문자열
hex_string = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

# 바이트열로 변환
data = bytes.fromhex(hex_string)

# 모든 키값(0~255)에 대해 XOR 수행
for key in range(256):
    # XOR 연산 결과
    decrypted = bytes([b ^ key for b in data])
    try:
        # 출력 시도 (ASCII로 디코딩)
        text = decrypted.decode('utf-8')
        print(f"Key: {key:3} | {text}")
    except UnicodeDecodeError:
        # 디코딩 실패 시 무시
        continue
