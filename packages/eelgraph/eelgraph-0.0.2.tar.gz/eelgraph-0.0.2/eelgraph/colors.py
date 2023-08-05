import random


def fill(col):
    return col.format("0.2")


def mid(col):
    return col.format("0.75")


def stroke(col):
    return col.format("1.0")


best = [
    "rgba(172, 34, 125, {0})",
    "rgba(238, 150, 42, {0})",
    "rgba(249, 213, 97, {0})",
    "rgba(0, 168, 90, {0})",
    "rgba(0, 195, 221, {0})"
]


def randomColor(colorSet, strokeB=False):
    pick = random.choice(colorSet)
    return pick


def randomColors(colorSet, data):
    out = []
    lastColor = None
    for _ in range(len(data)):
        pick = randomColor(colorSet)
        while (pick == lastColor) or (_ == len(data) - 1 and pick == out[0]):
            pick = randomColor(colorSet)
        out.append(pick)
        lastColor = pick
    return out
