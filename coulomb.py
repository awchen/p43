import argparse
import csv
import pylab as plt
import numpy as np
import time
import copy
from math import *

TIME_INTERVAL = 0.0001 #seconds
k = 8.988e9

class Charge:
    def __init__(self, name, charge, mass, pos, velocity):
        self.name = name
        self.q = charge # C
        self.m = mass # g
        self.pos = pos # (m, m, [m])
        self.v = velocity # (m/s, m/s, [m/s])
        self.a = (0, ) * len(velocity) # (m/s^2, m/s^2, [m/s^2])
        self.size = None

def parseFile(filepath):
    with open(filepath, 'r') as f:
        spec = csv.reader(f)
        next(spec)

        print "Parsed the following charges:"

        charges = []
        for row in spec:
            row = [elem.strip() for elem in row]
            name = row[0]
            charge = float(row[1])
            mass = float(row[2])

            curr = []
            for elem in row[3:-1]:
                curr.append( float(elem.strip('()')) )
                if elem[-1] == ')':
                    pos = tuple(curr)
                    curr = []
            curr.append( float(row[-1].strip('()')) )
            velocity = tuple(curr)

            print ("%s, q = %s, m = %s, position = %s, v = %s" % \
                    (name, charge, mass, pos, velocity))
            charges.append( Charge(name, charge, mass, pos, velocity) )
    return charges

def getViewpoint(charges):
    numAxes = len( charges[0].pos )
    diffs = []
    minMaxes = []
    for i in range(numAxes):
        vals = [ charge.pos[i] for charge in charges ]
        minVal = min(vals)
        maxVal = max(vals)
        dist = maxVal - minVal
        if dist == 0:
            dist = 1
        diffs.append(dist)
        minMaxes.append((minVal, maxVal))
    maxDiff = max(diffs)
    viewpoint = []
    for i in range(numAxes):
        viewpoint.append((minMaxes[i][1] + minMaxes[i][0])/2 - maxDiff * 2 )
        viewpoint.append((minMaxes[i][1] + minMaxes[i][0])/2 + maxDiff * 2)

    return viewpoint

def plot(plt, prev, charges, posOffset):
    for elem in prev:
        elem.remove()

    # [x], [y], [q]
    pos = ([], [], [])
    neg = ([], [], [])
    neut = ([], [], [])
    for c in charges:
        if c.q > 0:
            pos[0].append(c.pos[0])
            pos[1].append(c.pos[1])
            pos[2].append(c.size)
        elif c.q < 0:
            neg[0].append(c.pos[0])
            neg[1].append(c.pos[1])
            neg[2].append(c.size)
        else:
            neut[0].append(c.pos[0])
            neut[1].append(c.pos[1])
            neut[2].append(c.size)

    curr = []
    curr.append( plt.scatter(pos[0], pos[1], marker='o', color='red', s=pos[2]) )
    curr.append( plt.scatter(neg[0], neg[1], marker='o', color='blue', s=neg[2]) )
    curr.append( plt.scatter(neut[0], neut[1], marker='o', color='gray', s=neut[2]) )
    for c in charges:
        curr.append( plt.text(c.pos[0], c.pos[1]+ sqrt(c.size/3.14) / 2 + posOffset, "%s, %s C" % (c.name, c.q), \
                horizontalalignment='center') )

    plt.draw()
    plt.pause(TIME_INTERVAL)
    return curr

def force(q1, q2, r):
    return (k * q1 * q2) / (r**2)

# returns a difference vector (x, y, z) with direction a -> b
def diffVec(b, a):
    return tuple([ b[i]-a[i] for i in range(len(a)) ])

def addVec(a, b):
    return tuple([ b[i]+a[i] for i in range(len(a)) ])

# returns distance between vectors a and b
def distance(a, b):
    return sqrt( sum([ (b[i]-a[i])**2 for i in range(len(a)) ]) )

def length(a):
    return sqrt( sum([ a[i]**2 for i in range(len(a)) ]) )

def scaleVec(a, scale):
    return tuple([ a[i] * scale for i in range(len(a)) ])

def unitVec(a):
    return scaleVec(a, 1 / length(a))

def update(charges, timeInterval):
    newCharges = copy.deepcopy(charges)
    forces = [(0,) * len(charges[0].pos)] * len(charges)
    for i in range(len(charges)):
        for j in range(i+1, len(charges)):
            c1 = charges[i]
            c2 = charges[j]
            f12 = scaleVec( unitVec( diffVec(c2.pos, c1.pos) ), force(c1.q, c2.q, distance(c1.pos, c2.pos)) )
            f21 = scaleVec( f12, -1 )
            forces[i] = addVec(f21, forces[i])
            forces[j] = addVec(f12, forces[j])

    for i, new in enumerate(newCharges):
        old = charges[i]

        new.a = scaleVec( forces[i], 1 / old.m )
        new.v = addVec( old.v, scaleVec(new.a, timeInterval) )
        new.pos = addVec( old.pos, addVec( scaleVec(old.v, timeInterval), scaleVec(old.a, 0.5 * timeInterval**2) ) )
        if new.m != float("inf"):
            print new.pos

    return newCharges

def main():
    parser = argparse.ArgumentParser(description='Model the motion of charged particles.')
    parser.add_argument('filepath', nargs=1, \
            help='Path to the file containing the starting states for the particles.\n' \
               + 'The format of this file can be found in the README.')
    parser.add_argument('--t', type=float, nargs=1, \
            help='The amount of time in seconds to elapse between each state update.  Default 0.025.')

    args = parser.parse_args()

    filepath = args.filepath[0]
    charges = parseFile(filepath)
    
    allM = [c.m for c in charges]
    if len(allM) > 0:
        mRange = (min(allM), max(allM))
    else:
        mRange = (0, 0)
    if mRange[0] == mRange[1]:
        for c in charges:
            c.size = 20
    else:
        for c in charges:
            c.size = max(10, c.m * 150 / max(allM)) if c.m != float("inf") else 300

    plt.ion()
    viewpoint = getViewpoint(charges)
    plt.axis( viewpoint )
    posOffset = (viewpoint[3] - viewpoint[2]) / 100

    timeInterval = TIME_INTERVAL

    prev = []
    while(True):
        try:
            prev = plot(plt, prev, charges, posOffset)
            charges = update(charges, timeInterval)
        except KeyboardInterrupt:
            exit(0)

if __name__ == "__main__":
    main()