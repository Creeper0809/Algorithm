
history_set = {"social", "history", "language", "literacy"}
bigdata_set = {"bigdata", "public", "society"}

words = input().split()
for i in words:
    for j in history_set:
        if i.find(j) != -1:
            print("digital humanities")
            exit(0)
    for j in bigdata_set:
        if i.find(j) != -1:
            print("public bigdata")
            exit(0)
