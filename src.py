import random
import statistics
import copy
import numpy as np


def sCurve(x, g):
    return x * g / (g + x ** 2) ** (1 / 2)


def generateInput(p):
    # options = [[1, -1, -1, -1, 1, -1],
    #            [-1, 1, -1, -1, -1, 1],
    #            [-1, -1, 1, 1, -1, -1]]
    # o = [-1, -1, -1]
    # o[random.randint(0, 2)] = 1
    # for _ in range(p):
    #     o = o + options[random.randint(0, 2)]

    m = random.randint(0, 2)
    o = []
    for _ in range(p * 2):
        temp = [-1, -1, -1]
        val = random.randint(0, 5)
        if val > 2:
            val = m
        temp[val] = 1
        o = o + temp
    temp = [-1, -1, -1]
    temp[m] = 1

    return o + temp


def findOutput(weightsForOuts, ins, h):
    if len(weightsForOuts) != (1 + h):
        raise NameError('weights is not the same length as the input')
    outs = []
    for n in range(len(weightsForOuts)):
        if n < h:
            outs = [0 for _ in range(len(ins))]
            layer = weightsForOuts[n]
            for i in range(len(layer)):
                for j in range(len(layer)):
                    outs[j] += ins[i] * layer[i][j]
            ins = outs.copy()
        else:
            outs = [0 for _ in range(3)]
            for i in range(len(weightsForOuts)):
                for j in range(len(outs)):
                    outs[j] += ins[i] * weightsForOuts[h][i][j]
        for i in range(len(outs)):
            outs[i] = sCurve(outs[i], 1)
    return outs


def findWinner(p1, p2):
    choice1 = p1.index(max(p1))
    choice2 = p2.index(max(p2))
    if choice1 == choice2:
        return 0
    if choice1 == 2 and choice2 == 0 or choice1 + 1 == choice2:
        return 1
    return -1


def reproduce(pastGen, sigma):
    newGen = []
    for organism in pastGen:
        baby = copy.deepcopy(organism)
        for i in range(len(baby)):
            for j in range(len(baby[i])):
                for k in range(len(baby[i][j])):
                    baby[i][j][k] += np.random.normal(0, sigma)
                    baby[i][j][k] = sCurve(baby[i][j][k], 1)
        newGen.append(baby)
    return newGen
    # return [generateWeights(pastGames, hiddenLayers) for _ in range(len(pastGen))]


def generateWeights(p, h):
    o = [[[sCurve(random.random() * 2 - 1, 1) for _ in range(p * 6)] for _ in range(p * 6)] for _ in range(h)]
    o = o + [[[sCurve(random.random() * 2 - 1, 1) for _ in range(3)] for _ in range(p * 6)]]
    return o


def getPlayerMove():
    playerMove = 'r'
    while playerMove != 'r' and playerMove != 'p' and playerMove != 's':
        playerMove = input('r, p, s ')
    if playerMove == 'r':
        return [1, -1, -1]
    elif playerMove == 'p':
        return [-1, 1, -1]
    elif playerMove == 's':
        return [-1, -1, 1]
    else:
        raise NameError("you somehow chose an invalid move")


pastGames = 0
hiddenLayers = 1
generationSize = 20

inputLayer = []
nextGen = []

# while len(nextGen) < 20:
#     w = generateWeights(pastGames, hiddenLayers)
#     score = 0
#     for _ in range(100):
#         inputLayer = generateInput(pastGames)
#         move = inputLayer[-3:]
#         inputLayer = inputLayer[:-3]
#         outputLayer = findOutput(w, inputLayer.copy(), hiddenLayers)
#         score += findWinner(move, outputLayer)
#     print(score)
#     if score > 0:
#         nextGen.append(w)

for _ in range(generationSize):
    nextGen.append(generateWeights(10, hiddenLayers))

print("done setting up")

w, l, t = 0, 0, 0

for _ in range(100):
    computerChoice = []
    if pastGames == 10:
        print("learning")
    if pastGames > 10:
        for m in range(10):
            organisms = []
            scores = []
            for org in nextGen:
                score = 0
                for n in range(max(pastGames - 20, 0), pastGames - 10):
                    move = inputLayer[(n + 1) * 6:(n + 10) * 6 + 3]
                    scope = inputLayer[n * 6:(n + 10) * 6]
                    outputLayer = findOutput(org, scope.copy(), hiddenLayers)
                    score += findWinner(move, outputLayer)
                tup = score, org
                organisms.append(tup)
                scores.append(score)
            cutoff = statistics.median(scores)
            # print(np.mean(scores), max(scores))
            organisms = sorted(organisms, reverse=True)
            bestHalf = []
            for i in range(int(generationSize / 2)):
                bestHalf.append(organisms[i][1])

            nextGen = bestHalf + reproduce(bestHalf, 1)
            while len(nextGen) < 20:
                nextGen.append(generateWeights(10, hiddenLayers))

        scope = inputLayer[-60:]
        computerChoice = findOutput(nextGen[0], scope.copy(), hiddenLayers)
    else:
        computerChoice = [-1, -1, -1]
        computerChoice[random.randint(0, 2)] = 1
    playerChoice = getPlayerMove()
    inputLayer = inputLayer + computerChoice + playerChoice
    pastGames += 1

    outCome = findWinner(playerChoice, computerChoice)
    highest = max(computerChoice)
    computerChoice.remove(highest)
    print(highest, (highest - np.mean(computerChoice)) / 0.02)
    if outCome == 1:
        print("you lose")
        t += 1
    elif outCome == 0:
        print("tie")
        t += 1
    elif outCome == -1:
        print("you win")
        w += 1
