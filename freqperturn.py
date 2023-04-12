# freqperturn.py
# Dave Kingma
#
# This program assumes an Amitron T50-6 core is used (Al = 46), and given a whip length of A (ft), a distance of the
# loading coil from the bottom of the whip B, and a whip diameter of D (in). For every turn on the core,
# it calculates the resonant frequency (MHz), the inductance of the toroid L (uH), and the maximum diameter
# wire that can be used to make that number of turns such that the turns do not take up more than 300 degrees
# of the circumference of the toroid core.

import math

A = 3.875
#A = 6
B = 0
D = 0.237
#D = 0.24
Al = 46
coreSize = 50

maxTurns = {
    12:  {14: 0, 16: 0, 18: 0, 20: 0, 22: 1, 24: 3, 26: 5, 28: 8, 30: 11, 32: 15, 34: 20, 36: 26},
    16:  {14: 0, 16: 0, 18: 0, 20: 1, 22: 2, 24: 4, 26: 6, 28: 9, 30: 13, 32: 17, 34: 22, 36: 29},
    25:  {14: 0, 16: 1, 18: 3, 20: 5, 22: 7, 24: 10, 26: 14, 28: 18, 30: 24, 32: 31, 34: 41, 36: 52},
    37:  {14: 4, 16: 6, 18: 9, 20: 12, 22: 17, 24: 22, 26: 29, 28: 37, 30: 48, 32: 60, 34: 78, 36: 98},
    50:  {14: 8, 16: 12, 18: 16, 20: 22, 22: 28, 24: 37, 26: 47, 28: 59, 30: 76, 32: 94, 34: 121, 36: 151},
    68:  {14: 12, 16: 16, 18: 21, 20: 28, 22: 36, 24: 46, 26: 59, 28: 74, 30: 94, 32: 117, 34: 150, 36: 187},
    80:  {14: 17, 16: 23, 18: 30, 20: 39, 22: 51, 24: 64, 26: 82, 28: 103, 30: 129, 32: 161, 34: 204, 36: 255},
    94:  {14: 21, 16: 27, 18: 35, 20: 45, 22: 58, 24: 74, 26: 94, 28: 117, 30: 148, 32: 183, 34: 233, 36: 290},
    106: {14: 21, 16: 27, 18: 36, 20: 46, 22: 59, 24: 74, 26: 95, 28: 118, 30: 149, 32: 185, 34: 235, 36: 293},
    130: {14: 31, 16: 40, 18: 51, 20: 65, 22: 83, 24: 105, 26: 133, 28: 165, 30: 208, 32: 257, 34: 326, 36: 406},
    157: {14: 39, 16: 50, 18: 64, 20: 81, 22: 103, 24: 129, 26: 164, 28: 204, 30: 256, 32: 316, 34: 401, 36: 499},
    184: {14: 38, 16: 50, 18: 63, 20: 81, 22: 102, 24: 129, 26: 163, 28: 202, 30: 254, 32: 314, 34: 398, 36: 496},
    200: {14: 53, 16: 67, 18: 86, 20: 108, 22: 137, 24: 172, 26: 217, 28: 270, 30: 338, 32: 418, 34: 529, 36: 658}
}

def calcL(f, A, B, D):
    pi = math.pi
    c1 = 10 ** 6 / (68 * pi ** 2 * f ** 2)
    c2 = math.log(24 * (234/f - B) / D) - 1
    c3 = (1 - f * B / 234) ** 2 - 1
    c4 = 234 / f - B
    c5 = math.log(24 * (A - B) / D) - 1
    c6 = (f * (A - B) / 234) ** 2 - 1
    c7 = A - B
    L = c1 * ((c2 * c3 / c4) - (c5 * c6 / c7))
    return(L)

def calcLGivenN(N, Al):
    L = Al * (N / 100) ** 2
    return L

def find_max_AWG(coreSize, numTurns, maxTurns):
    max_turns_for_core = maxTurns[coreSize]
    for wire_size in range(14, 36+1, 2):
        if max_turns_for_core[wire_size] >= numTurns:
            return wire_size
    return None

maxTurnsCore = maxTurns[coreSize][36]
print("Turns, Frequency (MHz), L (uH), Max Wire Dia. (AWG)")
for N in range(1, maxTurnsCore, 1):
    targetL = calcLGivenN(N, Al)
    lowestError = 1000 # high enough number to start with
    resonantFrequency = 1.8
    start = .001
    stop = 100.0
    step = 0.001
    for i in range(int((stop-start)/step)+1):
        f = start + i * step
        L = calcL(f, A, B, D)
        if abs(targetL - L) < lowestError:
            lowestError = abs(targetL - L)
            resonantFrequency = f
    
    maxT50 = find_max_AWG(50, N, maxTurns)

    print(f"{N}, {resonantFrequency:.3f}, {targetL:.3f}, {maxT50}")
