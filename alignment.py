def alignStrings(match_n, mismatch_n, gapPenalty_n, stringA, stringB, isNW, isNWC, isNWR, isSW):
    mat = []
    if isNW:
        mat = alignNeedlemanWunsh(stringA, stringB, isNWC, isNWR, match_n, mismatch_n, gapPenalty_n)
    else:
        mat = alignSmithWaterman(stringA, stringB)
    printMatrix(stringA, stringB, mat)

def alignNeedlemanWunsh(stringA, stringB, isNWC, isNWR, match, mismatch, gapPenalty):
    matrix = []
    arrows = []
    lenA = len(stringA)+1
    lenB = len(stringB)+1
    for i in range(lenA):
        vector = []
        vectorArr = []
        for j in range(lenB):
            if j == 0:
                if isNWC:
                    vector.append(0)
                else:
                    vector.append(gapPenalty * i)
                if i > 0:
                    vectorArr.append(["u"])
                else:
                    vectorArr.append([])
            elif i == 0:
                if isNWR:
                    vector.append(0)
                else:
                    vector.append(gapPenalty * j)
                if j > 0:
                    vectorArr.append(["l"])
                else:
                    vectorArr.append([])
            else:
                result = maximizeValue(matrix[i-1][j-1], matrix[i-1][j], vector[j-1],
                                       stringA[i-1], stringB[j-1],
                                       match, mismatch, gapPenalty)
                vector.append(result[0])
                vectorArr.append(result[1])
        matrix.append(vector)
        arrows.append(vectorArr)
    return [matrix, arrows]

def maximizeValue(diagonal, up, left, A, B, match, mismatch, gapPenalty):
    if A == B:
        diagonal+=match
    else:
        diagonal+=mismatch
    up+=gapPenalty
    left+=gapPenalty
    value = diagonal
    arrows = ["d"]
    if up > value:
        value = up
        arrows = ["u"]
        if value == left:
            arrows.append("l")
    elif left > value:
        value = left
        arrows = ["l"]
        if value == up:
            arrows.append("u")
    elif value == up and value == left:
        arrows.append("u")
        arrows.append("l")
    elif value == left:
        arrows.append("l")
    elif value == up:
        arrows.append("u")
    return [value, arrows]



def alignSmithWaterman(stringA, stringB):
    matrix = []
    lenA = len(stringA)+1
    lenB = len(stringB)+1
    for i in range(lenA):
        vector = []
        for j in range(lenB):
            if j == 0:
                vector.append(0)
            elif i == 0:
                vector.append(0)
            else:
                vector.append(0)
        matrix.append(vector)
    return matrix

def printMatrix(stringA, stringB, result):
    mat = result[0]
    arrows = result[1]
    lenA = len(stringA) + 1
    lenB = len(stringB) + 1
    print("                e ", end='')
    for l in stringB:
        print("       "+l+" ", end='')
    print("\n")
    for i in range (lenA):
        if i == 0:
            print("       e ", end='')
        else:
            print("       "+stringA[i-1]+" ", end='')
        for j in range(lenB):
            print("       "+str(mat[i][j]), end='')
            for x in arrows[i][j]:
                print(x+" ", end='')
        print("\n")

