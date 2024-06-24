import model
import pickle
from time import perf_counter_ns

NANO_TO_SEC = 1000000000
INF = 100000
groups = []
patternDbDict = []

def init(boardSize):
    global groups
    global patternDbDict
    print(boardSize)
    print("Initializing pattern DB...")
    with open("patternDb_"+str(boardSize)+".dat", "rb") as patternDbFile:
        print("patternDb_"+str(boardSize)+".dat")
        groups = pickle.load(patternDbFile)
        patternDbDict = pickle.load(patternDbFile)
        for i in range(len(patternDbDict)):
            print("Group {}: {}, {:,} entries.".format(i,groups[i],len(patternDbDict[i])))

def idaStar(puzzle):
    if puzzle.checkWin():
        return []
    if not patternDbDict:
        init(puzzle.boardSize)

    t1 = perf_counter_ns()
    bound = hScore(puzzle)
    path = [puzzle]
    dirs = []
    max_depth = 0
    while True:
        rem, new_depth = search(path, 0, bound, dirs, 0)
        max_depth = max(max_depth, new_depth)
        if rem == True:
            tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
            print("Took {} seconds to find a solution of {} moves".format(tDelta, len(dirs)))
            return dirs, tDelta, max_depth
        elif rem == INF:
            return None
        bound = rem

def search(path, g, bound, dirs, max_depth):
    cur = path[-1]
    f = g + hScore(cur)
    max_depth = max(max_depth,g)

    if f > bound:
        return f, max_depth

    if cur.checkWin():
        return True, max_depth
    min = INF

    for dir in cur.DIRECTIONS:
        if dirs and (-dir[0], -dir[1]) == dirs[-1]:
            continue
        validMove, simPuzzle = cur.simulateMove(dir)

        if not validMove or simPuzzle in path:
            continue

        path.append(simPuzzle)
        dirs.append(dir)

        t, temp_depth = search(path, g + 1, bound, dirs, max_depth)
        max_depth = max(max_depth, temp_depth)
        if t == True:
            return True, max_depth
        if t < min:
            min = t

        path.pop()
        dirs.pop()

    return min, max_depth

def hScore(puzzle):
    h = 0
    for g in range(len(groups)):
        group = groups[g]
        hashString = puzzle.hash(group)
        if hashString in patternDbDict[g]:
            h += patternDbDict[g][hashString]
        else:
            print("No pattern found in DB, using manhattan dist")
            break
            for i in range(puzzle.boardSize):
                for j in range(puzzle.boardSize):
                    if puzzle[i][j] != 0 and puzzle[i][j] in group:
                        destPos = ((puzzle[i][j] - 1) // puzzle.boardSize,
                                     (puzzle[i][j] - 1) % puzzle.boardSize)
                        h += abs(destPos[0] - i)
                        h += abs(destPos[1] - j)

    return h
