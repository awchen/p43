# Extra credit submissions (achen28)

___

## \#1 Visualization of charged particle movement

#### Description

Visualizes the motion and interactions of multiple charged particles in a 2D plane.

Each charge has a point representation on the plane, with the area of the point scaled to the mass of the charge.  Positive, negative, and neutral charges are colored red, blue, and gray, respectively.  The axes' values are in meters.

Collisions between particles are not possible.

#### Usage

```
python coulomb.py filepath [--t interval] [-v]
```

`filepath` is a required argument that is the path to the input file that describes the starting states of the charges (format described below)

`--t interval` is an optional argument that specifies the time interval in seconds between state updates.  Larger values will enable the plot to be updated in real-time, at the cost of accuracy, while smaller values require more computational power but will result in more accurate state updates (more detail below).    `interval` must be a valid float.

`-v` is an optional flag that tells the script to print out the timestamped states of the charges after each update to `STDOUT`.

##### Usage Note

Because `matplotlib` is typically not used with live updates, there is no consistent method to cleanly exit from the program, and `SIGINT` is typically ineffective.  Therefore, the optimal method to exit the program is to kill the program with `CTRL + \`.

#### Input file format

The input files have the format of a CSV, with the columns

`name`, `charge (C)`, `mass (g)`, `position (m)`, `velocity (m/s)`

in that order.  `charge` and `mass` must be floats, while `position` and `velocity` must be a two-element tuple representing the components of a vector in R^2 with each element a float.  `charge` must have units of coulombs, `mass` must have units of grams, and the components of `position` and `velocity` must have units `m` and `m/s`, respectively.

Each line contains a description of a single charge, and the first line must be the header as shown in the examples.

#### Examples

There are six examples included for this program.

`bound` is a demonstration of bound motion for all particles, and also provides a good illustration of the time interval tradeoff (further described below).

`flyby` is a simple example demonstrating the ability for two moving charges to alter each other's directions.

`momentum` shows the oscillation of a charge between two stationary charges used to build up speed.

`neutral` illustrates how neutral charges don't exert a force on each other.

`opposing` demonstrates the repulsive nature of like charges.

`stationary` demonstrates that a charge with infinite mass doesn't move (who knew?).

#### Tradeoffs for `interval`: optimizing speed vs. accuracy

The program is designed such that it attempts to update the state of the charges every `interval` seconds.  For relatively large values of `interval` (around 0.01+), the state of the charges can be updated effectively in real time.  However, larger values of `interval` come with a decrease in accuracy.  This is because over each `interval`, the state of the charges cannot be updated.  Therefore, the acceleration and velocity of the charges must be assumed to be uniform over that period of time, which may not be the case in reality.

Conversely, smaller values of `interval` will allow for updating of the state of the charges at additional timepoints, which will allow for an increase in accuracy, because the `intervals` better model the infinitismally small time intervals that are required for 100% accurate updates of the states.  However, the increase in updates will also increase the program's demand for computational resources, and may run extremely slowly.

The effect of the size of `interval` is clearly demonstrated by the example `bound`.  The initial state of the charges in `bound` were explicitly constructed such that particle `b` would have uniform circular motion around `a` at a distance of 10 meters.  In this example, if `interval` is not infinitismally small, the position update will be inaccurate, because it is impossible to account for the fact that the direction of the centripetal force changes over an infinitismally small time period.  However, smaller values of `interval` better model this change.  To explicitly see this effect, we can run `bound` with an `interval` of 0.025 s, and an `interval` of 0.0001 s.  

With `interval = 0.025`, the rightmost (+x) point on the path that particle `b` takes in its first loop around `a` has a value `(10.15256136427193, -0.3243573124031124)`, which is 10.1577414 meters away from the center, for an error of 0.1577414 meters.

On the other hand, with `interval = 0.0001`, the rightmost point on the first loop that `b` takes has value `(10.000570926612356, -0.00018607259310355348)`, which is 10.0005709 meters from the center, for a substantially better error of 0.0005709 meters.
___

## \#2 Addressing the Parallel Capacitor Paradox

#### Description

This is a paper `Parallel_Paradox.pdf` that:

- Outlines the scientific premise of the parallel capacitor paradox
- Comprehensively derives a quantitative solution for the charge on the capacitors as a function of time
- Demonstrates with mathematical derivations that the usage of ohmic wires fully explains the "disappearance" of energy
- Explores a hypothesis involving inductance and electromagnetic waves to explain the decrease in energy between the capacitors given superconducting wires
