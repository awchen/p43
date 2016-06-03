import argparse
import csv
import pylab as plt
import numpy as np
import time
import copy

k = 8.988e9

class Charge:
    def __init__(self, name, charge, mass, pos, velocity, acceleration):
        self.name = name
        self.q = charge
        self.m = mass
        self.pos = pos
        self.v = velocity
        self.a = acceleration

def parseFile(filepath):
    with open(filepath, 'r') as f:
        spec = csv.reader(f)
        next(spec)

        charges = []
        for row in spec:
            row = [elem.strip() for elem in row]
            name = row[0]
            charge = float(row[1])
            mass = float(row[2])

            curr = []
            for i, elem in enumerate(row[3:-1]):
                curr.append( float(elem.strip('()')) )
                if elem[-1] == ')':
                    pos = tuple(curr)
                    curr = []
                    break
            for i, elem in enumerate(row[i+1:-1]):
                curr.append( float(elem.strip('()')) )
                if elem[-1] == ')':
                    velocity = tuple(curr)
                    curr = []
            curr.append( float(row[-1].strip('()')) )
            acceleration = tuple(curr)

            print name, charge, mass, pos, velocity, acceleration

            charges.append( Charge(name, charge, mass, pos, velocity, acceleration) )
    return charges

def getViewpoint(charges):
    viewpoint = []
    numAxes = len( charges[0].pos )
    for i in range(numAxes):
        vals = [ charge.pos[i] for charge in charges ]
        minVal = min(vals)
        maxVal = max(vals)
        dist = maxVal - minVal
        if dist == 0:
            dist = 1
        viewpoint.append( minVal - dist )
        viewpoint.append( maxVal + dist )
    return viewpoint

def plot(plt, prev, charges):
    for elem in prev:
        elem.remove()

    # [x], [y], [q]
    pos = ([], [], [])
    neg = ([], [], [])
    for c in charges:
        if c.q > 0:
            pos[0].append(c.pos[0])
            pos[1].append(c.pos[1])
            pos[2].append(c.q)
        elif c.q < 0:
            neg[0].append(c.pos[0])
            neg[1].append(c.pos[1])
            neg[2].append(abs(c.q))

    curr = []
    if len(pos[0]) > 0:
        curr.append( plt.scatter(pos[0], pos[1], marker='o', color='red', s=pos[2]) )
    if len(neg[0]) > 0:
        curr.append( plt.scatter(neg[0], neg[1], marker='o', color='blue', s=neg[2]) )

    plt.draw()
    plt.pause(0.01)
    return curr

def force(q1, q2, r):
    return (k * q1 * q2) / (r**2)

# returns a difference vector (x, y, z) with direction a -> b
def diffVec(a, b):
    return tuple([ b[i]-a[i] for i in range(len(a)-1, -1, -1) ])

# returns distance between vectors a and b
def distance(a, b):
    return sqrt( sum([ (b[i]-a[i])**2 for i in range(len(a)) ]) )

def length(a):
    return sqrt( sum([ a[i]**2 for i in range(len(a)) ]) )

def scaleVec(a, scale):
    return tuple([ a[i] * scale for i in range(len(diffVec)) ])

def unitVec(a):
    return scaleVec(a, 1 / length)

def update(charges):
    new = copy.deepcopy([])
    for i in range(len(charges)):
        for j in range(i+1, len(charges)):
            iVec = i.pos

def main():
    parser = argparse.ArgumentParser(description='Model the motion of charged particles.')
    parser.add_argument('filepath', nargs=1, \
            help='Path to the file containing the starting states for the particles.\n' \
               + 'The format of this file can be found in the README.')

    args = parser.parse_args()

    filepath = args.filepath[0]
    charges = parseFile(filepath)

    plt.ion()
    plt.axis( getViewpoint(charges) )

    prev = []
    while(True):
        try:
            prev = plot(plt, prev, charges)
            update(charges)
        except KeyboardInterrupt:
            exit(0)

if __name__ == "__main__":
    main()