N = int(input("N = "))
e = int(input("e = "))
flag_enc = int(input("flag_enc = "))

C = (flag_enc * pow(2, e, N) % N)
print(hex(C))

decrypted_C = int(input("decrypted_C = "))

M = (decrypted_C * pow(2, -1, N) % N)

print(M)
flag_bytes = M.to_bytes((M.bit_length()+7)//8, "big")
print(flag_bytes.decode())
