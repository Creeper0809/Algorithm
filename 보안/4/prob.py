from pwn import remote
import ast

count    = 0
max_num  = 0
result   = []

while True:
    p = remote('host3.dreamhack.games', 18640)
    line = p.recvline().decode().strip()
    arr  = ast.literal_eval(line)
    p.close()

    if count >= len(arr):
        break

    max_num = max(max_num, arr[count])
    print(f"[idx={count}] max={max_num}, diff={max_num - arr[count]}")

    if max_num - arr[count] == 51:
        result.append(arr[count])
        max_num = 0
        count += 1

flag = ''.join(chr(x) for x in result)
print("result bytes:", result)
print("flag string:", flag)
