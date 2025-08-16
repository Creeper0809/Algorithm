i = 1
while True:
    i += 1
    result = 200 * (1-(0.997**i))
    print(i,result)
    if result % 10 == 0:
        print(i,result)

    if result == 200:
        print(i,result)
        break