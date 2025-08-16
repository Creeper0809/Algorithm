def solution(ingredient):
    answer = 0
    hamarr = []
    for i in ingredient:
        hamarr.append(i)
        if hamarr[-4:] == [1,2,3,1]:
            answer += 1
            del hamarr[-4:]
    return answer