import random
import os


d1 = {}  # add as soon as PI finds it, then remove as soon as another PI finds it, holds a pos
seen = set()
allPI = {}  # add every PI to it, remove as soon as d1 is gone through, then heapify and do 3
unvisited = set()  # has all 1 pos, remove as soon as found (for 4) (size,key)
EPI = set()  # set of EPI terms
booleanEQ = []
largecomment = """
input is arr
output is boolean logic

fully parse array
go through d1 list, find all necessary EPI
go through sorted list of sets by size, removing all values in set from unvisited set as u move
remove all in unvisited set

d1 stores EPI tuple, as map 
when found, delete

"""

def initialize():
    d1.clear()
    seen.clear()
    allPI.clear()
    unvisited.clear()
    EPI.clear()
    booleanEQ.clear()

def getGrayPos(num):
    def grayRot(v):
        if v == 2:
            return 3
        if v == 3:
            return 2
        return v
    r = grayRot(num%4)
    c = grayRot(num//4)
    return (r,c)

def findShape(arr, pos, size):  # take in pos(r,c), size(2,22,4,8,44)
    r = pos[0]
    c = pos[1]
    output = []
    if size == 1:
        initH = [[0,0]]
        w, h = 1, 1
        initV = []
    elif size == 2:
        initH = [[0, 0], [0, -1]]
        w, h = 2, 1
        initV = [[0, 0], [-1, 0]]
    elif size == 22:
        initH = [[0, 0], [0, -1]]
        w, h = 2, 2
        initV = [[-1, -1], [-1, 0]]
    elif size == 4:
        initH = [[0, 0]]
        w, h = 4, 1
        initV = [[0, 0]]
    elif size == 8:
        initH = [[0, 0], [-1, 0]]
        w, h = 4, 2
        initV = [[0, 0], [0, -1]]
    elif size == 16:
        initH = [[0, 0]]
        w, h = 4, 4
        initV = []
    else:
        return []
    for rS, cS in initH:
        currBox = []
        oneCount = 0
        exit = False
        for i in range(w):
            if not exit:
                for j in range(h):
                    newR = (rS+r+j) % 4
                    newC = (cS+c+i) % 4
                    val = arr[newR][newC]
                    if arr[newR][newC] == 1:
                        oneCount += 1
                    currBox.append((newR, newC))
                    if val == "0":
                        exit = True
                        break
        if not exit:
            output.append((currBox,oneCount))
    for rS, cS in initV:
        currBox = []
        oneCount = 0
        exit = False
        for i in range(h):
            if not exit:
                for j in range(w):
                    newR = (rS+r+j) % 4
                    newC = (cS+c+i) % 4
                    val = arr[newR][newC]
                    if arr[newR][newC] == 1:
                        oneCount += 1
                    currBox.append((newR, newC))
                    if val == "0":
                        exit = True
                        break
        if not exit:
            output.append((currBox,oneCount))
    return output

# 1 take a pos if 1
# 2 return largest shape/s from that pos
# 3 go through max heap of shape sizes
# 4 cover all 1s


def makeArr(oneList,xList):
    arr = [["0"]*4 for i in range(4)]
    for val in oneList:
        if val:
            pos = getGrayPos(int(val))
            arr[pos[0]][pos[1]] = "1"
    for val in xList:
        if val:
            pos = getGrayPos(int(val))
            arr[pos[0]][pos[1]] = "X"
    return arr

def randArr():
    randArr = [random.randint(0, 9) for _ in range(16)]
    arr = [["0"]*4 for i in range(4)]
    for idx, el in enumerate(randArr):
        if el <= 3:
            arr[idx//4][idx % 4] = "1"
        elif el <= 6:
            arr[idx//4][idx % 4] = "0"
        else:
            arr[idx//4][idx % 4] = "X"

    return arr


def printK(arr):
    print("    00    01    11    10")
    ham = ["00", "01", "11", "10"]
    for row in arr:
        print(ham.pop(0), end="   ")
        for val in row:
            print(val, end="     ")
        print()
        print()


def runKTesting():
    i = ""
    counter = 0
    while(i != "Q"):
        initialize()
        i = input("Input (random, given, Q):  ")
        if i == "random":
            os.system('cls' if os.name == 'nt' else 'clear')
            counter += 1
            print('K-map ', counter, ':')
            print('_________________________')
            print()
            arr = randArr()
            printK(arr)
            PIFinder(arr)
            i = input("Solve? (enter to continue)")
            print()
            solverPrint()
        elif i == "given":
            os.system('cls' if os.name == 'nt' else 'clear')
            oneList = input("List of 1's (comma-separated, gray-counted)\n").split(',')
            xList = input("List of X's (comma-separated, gray-counted)\n").split(',')
            arr = makeArr(oneList,xList)
            print('K-map: ')
            print('_________________________')
            print()
            printK(arr)
            PIFinder(arr)
            print()
            solverPrint()




def PItoTerm(PI):
    maxSet = {'!A', 'A', '!B', 'B', '!C', 'C', '!D', 'D'}
    for point in PI:
        wordSet = set()
        if point[0] == 1 or point[0] == 2:
            wordSet.add('D')
        else:
            wordSet.add('!D')
        if point[0] == 2 or point[0] == 3:
            wordSet.add('C')
        else:
            wordSet.add('!C')
        if point[1] == 1 or point[1] == 2:
            wordSet.add('B')
        else:
            wordSet.add('!B')
        if point[1] == 2 or point[1] == 3:
            wordSet.add('A')
        else:
            wordSet.add('!A')
        maxSet = maxSet & wordSet
    return ''.join(sorted(list(maxSet),key=lambda t:t[-1]))


def PIFinder(arr):
    sizes = [16, 8, 4, 2, 1]
    # parse array
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == "1":
                unvisited.add((i, j))
                tempPIs = []
                for size in sizes:
                    tempPIs = findShape(arr, (i, j), size)
                    if size == 4:
                        tempPIs += findShape(arr, (i, j), 22)
                    if len(tempPIs) != 0:
                        break
                for PI,oneCount in tempPIs:
                    PI.sort()
                    tup = tuple(PI)
                    if tup not in allPI:
                        allPI[tup] = oneCount
                        for point in PI:
                            if point in d1:
                                d1.pop(point)
                            if point not in seen and arr[point[0]][point[1]] == "1":
                                d1[point] = tup
                            seen.add(point)
    tempPI = allPI.copy()
    for PI in d1.keys():
        EPI.add(d1[PI])
        if d1[PI] in tempPI:
            unvisited.difference_update(set(d1[PI]))
            booleanEQ.append(PItoTerm(d1[PI]))
            tempPI.pop(d1[PI])
    tempList = list(tempPI.keys())
    tempList.sort(key=lambda t: (len(t),allPI[t]), reverse=True)
    for tup in tempList:
        if len(unvisited.intersection(set(tup))) != 0:
            unvisited.difference_update(set(tup))
            booleanEQ.append(PItoTerm(tup))
            if len(unvisited) == 0:
                break


def solverPrint():
    print("Prime Implicants (", len(allPI), "): ")
    print("________________________________")
    print()
    for PI in allPI:
        print(f"{PItoTerm(PI):>6}   -->   {PI}")
    print()
    print("Essential Prime Implicants (", len(EPI), "): ")
    print("________________________________")
    print()
    for PI in EPI:
        print(f"{PItoTerm(PI):>6}   -->   {PI}")
    print()
    print("Distinguished 1-Cells (", len(d1), "): ")
    print("________________________________")
    print()
    for point in d1.keys():
        print(point)
    print()
    print("The Boolean Equation")
    print("________________________________")
    print()
    print('+'.join(booleanEQ))
    print()
    print()




runKTesting()


