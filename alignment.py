def alignStrings(match_n, mismatch_n, gapPenalty_n, stringA, stringB, isNW, isNWC, isNWR, isNWF, isSW):
    mat = []
    if isNW:
        mat = alignNeedlemanWunsh(stringA, stringB, isNWC, isNWR, match_n, mismatch_n, gapPenalty_n)
        printMatrix(stringA, stringB, mat)
        alignment = readGlobalAlignment(mat[0], mat[1], isNWF, stringA, stringB)
    else:
        mat = alignSmithWaterman(stringA, stringB)
    # alig

    return[mat[0], mat[1], alignment]

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


def readGlobalAlignment(mat, arrows, isNWF, stringA, stringB):
    i = len(stringA)
    j = len(stringB)
    newAlignmentA = ""
    newAlignmentB = ""
    # ATTGTGATC
    # GTACATTCT
    result = getMaxScoring(mat[i],isNWF, i, j)
    scoring = result[0]
    j = result[1]
    if j < len(stringB):
        for k in range(len(stringB)-j):
            newAlignmentB+=stringB[j-k-1]
            newAlignmentA+="_"
    while (i >= 0 and j >= 0):
        arrowVec=  arrows[i][j]
        if len(arrowVec) > 0:
            for a in arrowVec:
                if a == "d":
                    newAlignmentB += stringB[j - 1]
                    newAlignmentA += stringA[i-1]
                    j -= 1
                    i -= 1
                elif a == "l":
                    #stringA is column
                    #stringB is row
                    newAlignmentB+= stringB[j-1]
                    newAlignmentA+= "_"
                    j -= 1
                elif a == "u":
                    newAlignmentB += "_"
                    newAlignmentA += stringA[i-1]
                    i -= 1
        else:
            i = -1
            j = -1
    return [newAlignmentB[::-1], newAlignmentA[::-1], scoring]

def getMaxScoring(vector, isNWF, i, j):
    maxValue = vector[j]
    index = 0
    newJ = j
    if isNWF:
        for x in vector:
            if x > maxValue:
                maxValue = x
                newJ = index
            index += 1
    return [maxValue, newJ]



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

