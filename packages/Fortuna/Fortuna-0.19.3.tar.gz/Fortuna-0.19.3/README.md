# Fortuna Beta: Fast & Flexible Random Value Generator
**Adventures in Predictable Non-determinism** \
More than just a high performance random number generator. \
Fortuna can help you build dynamic rarefied random value generators and more. \
See the random treasure examples in `.../fortuna_extras/fortuna_examples.py`

**Notes** \
Public Beta: _Fortuna is under active development, and may evolve without notice._ \
Ranges: _All ranges are inclusive unless stated otherwise._ \
Installation: _Open your favorite unix terminal and type_ `pip install Fortuna` or build from source.

## Fortuna Random Functions
### Random Numbers
`Fortuna.random_range(lo: int, hi: int) -> int` \
Returns a random integer in range `[lo..hi]` inclusive. \
Up to 15x faster than `random.randint()` \
Flat uniform distribution.

`Fortuna.random_below(num: int) -> int` \
Returns a random integer in the exclusive range `[0..num)` for positive values of num. \
Returns a random integer in the exclusive range `(num..0]` for negative values of num. \
This function never returns the value of num except in the case where `num == 0` \
As a result, it will always return zero if num is in range `[-1..1]` \
Flat uniform distribution.

`Fortuna.d(sides: int) -> int` \
Represents a single die roll of a given size die. \
Returns a random integer in the range `[1..sides]` \
Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int` \
Returns a random integer in range `[X..Y]` where `X == rolls` and `Y == rolls * sides` \
Represents the sum of multiple rolls of the same size die. \
Geometric distribution based on the number and size of the dice rolled. \
Complexity scales primarily with the number of rolls, not the size of the dice.

`Fortuna.plus_or_minus(num: int) -> int` \
Negative and positive input values of num will produce equivalent distributions. \
Returns random integer in the range `[-N..N]` where `N = abs(num)` \
Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int` \
Negative and positive input values of num will produce equivalent distributions. \
Returns random integer in the range `[-N..N]` where `N = abs(num)` \
Zero peak geometric distribution, triangle.

`Fortuna.plus_or_minus_curve(num: int, bounded: bool=True) -> int` \
Negative and positive input values of num will produce equivalent distributions. \
Returns a random integer in the target range `[-num..num]` \
If bounded is False, less than 0.1% of the results will fall outside the target range by up to +/- num. \
This will not change the overall shape of the distribution curve. \
Zero centered gaussian distribution, stretched bell curve: mean = 0, variance = num / pi

`Fortuna.zero_flat(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Flat uniform distribution.

`Fortuna.zero_cool(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Zero peak, geometric distribution, half triangle.

`Fortuna.zero_extreme(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Zero peak, gaussian distribution, half bell curve: mean = 0, variance = num / pi

`Fortuna.max_cool(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Max peak (num), geometric distribution, half triangle.

`Fortuna.max_extreme(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Max peak (num), gaussian distribution, half bell curve: mean = num, variance = num / pi

`Fortuna.mostly_middle(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Middle peak (num / 2), geometric distribution, half triangle.

`Fortuna.mostly_center(num: int) -> int` \
Returns a random integer in range `[0..num]` or `[num..0]` if num is negative. \
Middle peak (num / 2), gaussian distribution, bell curve: mean = num / 2, variance = num / pi

### Random Truth
`Fortuna.percent_true(num: int) -> bool` \
Always returns False if num is 0 or less, always returns True if num is 100 or more. \
Any value of num in range `[1..99]` will produce True or False. \
Returns a random Bool based on the probability of True as a percentage.

### Random Sequence Values
`Fortuna.random_value(arr) -> value` \
Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. \
Up to 10x faster than random.choice()

`Fortuna.pop_random_value(arr: list) -> value` \
Returns and removes a random value from a sequence list, uniform distribution, destructive. \
This function is not included in the Fortuna test suite due to it's destructive nature. \
This is the only destructive function in the module, use with care. It will raise an error if the list is empty.

### Random Table Values
`Fortuna.cumulative_weighted_choice(table) -> value` \
Core function for the WeightedChoice base class. \
Produces a custom distribution of values based on cumulative weights. \
Requires input format: `[(weight, value), ... ]` sorted in ascending order by weight. \
Weights must be unique positive integers. \
See WeightedChoice class for a more comprehensive solution that verifies and optimizes the table. \
Up to 15x faster than random.choices()

### Utility Functions
`Fortuna.min_max(num: int, lo: int, hi: int) -> int` \
Used to force a number in to the range `[lo..hi]` \
Returns num if it is already in the proper range. \
Returns lo if num is less than lo. Returns hi if num is greater than hi.

`Fortuna.analytic_continuation(func: staticmethod, num: int) -> int` \
Used to map a positive only function to the negative number line for complete input domain coverage. \
The "C" version of this function is used throughout the Fortuna extension. \
The function to be analytically continued must take an integer as input and return an integer.

## Fortuna Random Classes
### Sequence Wrappers
#### Random Cycle: The Truffle Shuffle
Returns a random value from the sequence. Produces a uniform distribution with no consecutive duplicates 
and relatively few nearly-consecutive duplicates. Longer sequences will naturally push duplicates even farther apart. 
This behavior gives rise to output sequences that seem much less mechanical than other random value sequences. 

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the sequence.
```python
from Fortuna import RandomCycle

random_cycle = RandomCycle(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])
random_cycle()  # returns a random value, cycled uniform distribution.
```

#### The Quantum Monty
A set of strategies for producing random values from a sequence where the probability \
of each value is based on the monty you choose. For example: the mostly_front monty \
produces random values where the beginning of the sequence is geometrically more common than the back. \
The Quantum Monty Algorithm results from overlapping the probability waves of six of the other eight methods. \
The distribution it produces is a gentle curve with a bump in the middle.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may vary slightly.
```python
from Fortuna import QuantumMonty

quantum_monty = QuantumMonty(["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"])
# Each of the following methods will return a random value from the sequence in it's own unique way.
quantum_monty.mostly_front()    # Mostly from the front of the list (geometric descending)
quantum_monty.mostly_middle()   # Mostly from the middle of the list (geometric pyramid)
quantum_monty.mostly_back()     # Mostly from the back of the list (geometric ascending)
quantum_monty.mostly_first()    # Mostly from the very front of the list (stretched gaussian descending)
quantum_monty.mostly_center()   # Mostly from the very center of the list (stretched gaussian bell curve)
quantum_monty.mostly_last()     # Mostly from the very back of the list (stretched gaussian ascending)
quantum_monty.quantum_monty()   # Quantum Monty Algorithm (all of the above)
quantum_monty.mostly_flat()     # Uniform flat distribution (see Fortuna.random_value)
quantum_monty.mostly_cycle()    # Cycled uniform flat distribution (see RandomCycle)
```

### Table & Dictionary Wrappers
#### Weighted Choice: Custom Rarity
Two strategies for selecting random values from a sequence where rarity counts. \
Both produce a custom distribution of values based on the weights of the values. \
Up to 10x faster than random.choices()

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance for large data sets.
- The sequence must not be empty, and each pair must have a weight and a value.
- Weights must be integers. A future release may allow weights to be floats.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check. 
As a result: non-unique values will have their probabilities logically accumulated. 
Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance. 
The choice to use one strategy over the other is purely about which one suits you or your data best.
Relative weights are easier to understand at a glance.
However, RPG Treasure Tables map rather nicely to a cumulative weighted strategy.

##### Cumulative Weight Strategy
_Note: Logic dictates Cumulative Weights must be unique!_
```python
from Fortuna import CumulativeWeightedChoice

cumulative_weighted_choice = CumulativeWeightedChoice((
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
))
cumulative_weighted_choice()  # returns a weighted random value
```

##### Relative Weight Strategy
```python
from Fortuna import RelativeWeightedChoice

relative_weighted_choice = RelativeWeightedChoice((
    (7, "Apple"),
    (4, "Banana"),
    (2, "Cherry"),
    (10, "Grape"),
    (3, "Lime"),
    (4, "Orange"),
))
relative_weighted_choice()  # returns a weighted random value
```

#### FlexCat
FlexCat wraps an OrderedDict of keyed sequences, and takes two optional keyword arguments, y_bias and x_bias.
FlexCat requires at least three keyed sequences each with at least 3 values.
The Y axis keys are accessed directly at call time, or randomized with one of the QuantumMonty methods, specified by y_bias.
The X axis sequences are randomized with one of the QuantumMonty methods, specified by x_bias.

By default FlexCat will use `y_bias="front"` and `x_bias="cycle"` if not specified at initialization. 
This will make the top of the data structure geometrically more common than the bottom, and it produces a flat 
cycled distribution for each category. The name FlexCat is short for flexible category sequence value generator.

Options for x & y bias: _See QuantumMonty for details_
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, stretched gaussian descending
- center, stretched gaussian bell curve
- last, stretched gaussian ascending
- flat, uniform flat
- cycle, cycled uniform flat
- monty, Quantum Monty Algorithm: steady with a bump in the middle.

```python
from Fortuna import FlexCat
from collections import OrderedDict

flex_cat = FlexCat(
    OrderedDict({
        "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
        "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
        "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
    }), y_bias="cycle", x_bias="cycle"
)
flex_cat("Cat_A")  # returns random value from "Cat_A" : cycled uniform distribution
flex_cat("Cat_B")  # returns random value from "Cat_B" : cycled uniform distribution
flex_cat("Cat_C")  # returns random value from "Cat_C" : cycled uniform distribution
flex_cat()         # returns random value from randomly cycled category : cycled uniform distribution
```

## Fortuna Sample Distribution and Performance Test Suite
_Testbed: MacOS 10.14.1, Python3.7, Quad 2.7GHz i7 Skylake, 16GB RAM, 1TB SSD_
<pre>
Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 10000: Total time: 14.954 ms, Average time: 1495 nano
 1: 9.74%
 2: 9.88%
 3: 9.31%
 4: 9.81%
 5: 10.25%
 6: 10.34%
 7: 9.98%
 8: 10.33%
 9: 10.56%
 10: 9.8%

random_range(1, 10) x 10000: Total time: 0.943 ms, Average time: 94 nano
 1: 9.64%
 2: 10.28%
 3: 9.98%
 4: 10.25%
 5: 9.88%
 6: 10.58%
 7: 9.64%
 8: 9.89%
 9: 9.93%
 10: 9.93%

Base Case:
random.randrange(10) x 10000: Total time: 9.968 ms, Average time: 997 nano
 0: 9.93%
 1: 10.27%
 2: 10.06%
 3: 9.74%
 4: 10.12%
 5: 9.78%
 6: 9.94%
 7: 9.9%
 8: 9.9%
 9: 10.36%

random_below(10) x 10000: Total time: 0.793 ms, Average time: 79 nano
 0: 10.01%
 1: 9.78%
 2: 10.3%
 3: 9.87%
 4: 9.84%
 5: 10.29%
 6: 9.97%
 7: 10.71%
 8: 9.56%
 9: 9.67%

d(10) x 10000: Total time: 0.821 ms, Average time: 82 nano
 1: 10.05%
 2: 10.05%
 3: 9.54%
 4: 10.46%
 5: 10.05%
 6: 10.21%
 7: 9.91%
 8: 10.16%
 9: 10.04%
 10: 9.53%

dice(2, 6) x 10000: Total time: 0.986 ms, Average time: 99 nano
 2: 2.62%
 3: 5.4%
 4: 8.6%
 5: 11.47%
 6: 14.11%
 7: 16.76%
 8: 13.02%
 9: 11.25%
 10: 8.35%
 11: 5.72%
 12: 2.7%

plus_or_minus(5) x 10000: Total time: 0.687 ms, Average time: 69 nano
 -5: 9.06%
 -4: 9.77%
 -3: 9.01%
 -2: 8.97%
 -1: 8.8%
 0: 9.03%
 1: 8.78%
 2: 9.14%
 3: 9.07%
 4: 9.31%
 5: 9.06%

plus_or_minus_linear(5) x 10000: Total time: 0.967 ms, Average time: 97 nano
 -5: 2.86%
 -4: 5.23%
 -3: 8.58%
 -2: 10.62%
 -1: 14.5%
 0: 16.33%
 1: 14.22%
 2: 10.64%
 3: 8.41%
 4: 5.64%
 5: 2.97%

plus_or_minus_curve(5) x 10000: Total time: 1.163 ms, Average time: 116 nano
 -5: 0.19%
 -4: 1.13%
 -3: 4.25%
 -2: 11.72%
 -1: 20.95%
 0: 25.02%
 1: 19.55%
 2: 11.63%
 3: 4.33%
 4: 0.95%
 5: 0.28%

zero_flat(10) x 10000: Total time: 0.687 ms, Average time: 69 nano
 0: 8.43%
 1: 8.74%
 2: 9.14%
 3: 9.01%
 4: 9.64%
 5: 8.97%
 6: 8.83%
 7: 9.48%
 8: 9.12%
 9: 9.19%
 10: 9.45%

zero_cool(10) x 10000: Total time: 1.654 ms, Average time: 165 nano
 0: 17.37%
 1: 15.02%
 2: 13.93%
 3: 11.55%
 4: 10.49%
 5: 9.01%
 6: 7.81%
 7: 6.09%
 8: 4.37%
 9: 2.94%
 10: 1.42%

zero_extreme(10) x 10000: Total time: 1.823 ms, Average time: 182 nano
 0: 22.29%
 1: 21.28%
 2: 17.72%
 3: 14.08%
 4: 10.69%
 5: 6.39%
 6: 3.9%
 7: 2.17%
 8: 0.94%
 9: 0.42%
 10: 0.12%

max_cool(10) x 10000: Total time: 1.871 ms, Average time: 187 nano
 0: 1.52%
 1: 3.03%
 2: 4.7%
 3: 5.9%
 4: 7.65%
 5: 9.07%
 6: 10.71%
 7: 12.43%
 8: 13.86%
 9: 14.53%
 10: 16.6%

max_extreme(10) x 10000: Total time: 1.907 ms, Average time: 191 nano
 0: 0.14%
 1: 0.5%
 2: 0.94%
 3: 2.08%
 4: 3.97%
 5: 6.57%
 6: 9.97%
 7: 13.71%
 8: 18.75%
 9: 21.21%
 10: 22.16%

mostly_middle(10) x 10000: Total time: 1.031 ms, Average time: 103 nano
 0: 2.71%
 1: 5.68%
 2: 7.83%
 3: 11.31%
 4: 13.94%
 5: 16.31%
 6: 13.85%
 7: 11.33%
 8: 8.85%
 9: 5.37%
 10: 2.82%

mostly_center(10) x 10000: Total time: 1.237 ms, Average time: 124 nano
 0: 0.21%
 1: 1.19%
 2: 4.39%
 3: 11.17%
 4: 19.91%
 5: 25.66%
 6: 20.21%
 7: 11.42%
 8: 4.29%
 9: 1.28%
 10: 0.27%


Random Truth
-------------------------------------------------------------------------

percent_true(25) x 10000: Total time: 0.694 ms, Average time: 69 nano
 False: 75.64%
 True: 24.36%


Random Values from a Sequence
-------------------------------------------------------------------------

some_list = ('Alpha', 'Beta', 'Delta', 'Eta', 'Gamma', 'Kappa', 'Zeta')

Base Case:
random.choice(some_list) x 10000: Total time: 7.967 ms, Average time: 797 nano
 Alpha: 14.0%
 Beta: 14.12%
 Delta: 14.27%
 Eta: 14.68%
 Gamma: 13.81%
 Kappa: 14.7%
 Zeta: 14.42%

random_value(some_list) x 10000: Total time: 0.709 ms, Average time: 71 nano
 Alpha: 14.25%
 Beta: 14.38%
 Delta: 14.88%
 Eta: 13.98%
 Gamma: 14.37%
 Kappa: 13.6%
 Zeta: 14.54%

monty = QuantumMonty(some_list)

monty.mostly_front() x 10000: Total time: 2.034 ms, Average time: 203 nano
 Alpha: 25.77%
 Beta: 21.81%
 Delta: 17.2%
 Eta: 14.34%
 Gamma: 10.5%
 Kappa: 6.86%
 Zeta: 3.52%

monty.mostly_middle() x 10000: Total time: 1.724 ms, Average time: 172 nano
 Alpha: 6.3%
 Beta: 12.95%
 Delta: 18.27%
 Eta: 24.69%
 Gamma: 19.0%
 Kappa: 12.69%
 Zeta: 6.1%

monty.mostly_back() x 10000: Total time: 2.233 ms, Average time: 223 nano
 Alpha: 3.57%
 Beta: 7.13%
 Delta: 10.23%
 Eta: 14.56%
 Gamma: 17.6%
 Kappa: 21.4%
 Zeta: 25.51%

monty.mostly_first() x 10000: Total time: 2.622 ms, Average time: 262 nano
 Alpha: 34.11%
 Beta: 30.19%
 Delta: 20.11%
 Eta: 10.3%
 Gamma: 3.88%
 Kappa: 1.16%
 Zeta: 0.25%

monty.mostly_center() x 10000: Total time: 1.906 ms, Average time: 191 nano
 Alpha: 0.35%
 Beta: 5.49%
 Delta: 23.83%
 Eta: 40.52%
 Gamma: 24.03%
 Kappa: 5.27%
 Zeta: 0.51%

monty.mostly_last() x 10000: Total time: 2.499 ms, Average time: 250 nano
 Alpha: 0.23%
 Beta: 1.17%
 Delta: 3.97%
 Eta: 10.28%
 Gamma: 19.92%
 Kappa: 29.77%
 Zeta: 34.66%

monty.quantum_monty() x 10000: Total time: 3.198 ms, Average time: 320 nano
 Alpha: 12.12%
 Beta: 13.02%
 Delta: 16.01%
 Eta: 18.88%
 Gamma: 15.4%
 Kappa: 13.26%
 Zeta: 11.31%

monty.mostly_flat() x 10000: Total time: 1.338 ms, Average time: 134 nano
 Alpha: 13.95%
 Beta: 15.06%
 Delta: 13.87%
 Eta: 14.05%
 Gamma: 14.42%
 Kappa: 14.04%
 Zeta: 14.61%

monty.mostly_cycle() x 10000: Total time: 6.426 ms, Average time: 643 nano
 Alpha: 14.28%
 Beta: 14.39%
 Delta: 14.21%
 Eta: 14.36%
 Gamma: 14.15%
 Kappa: 13.97%
 Zeta: 14.64%

random_cycle = RandomCycle(some_list)

random_cycle() x 10000: Total time: 5.661 ms, Average time: 566 nano
 Alpha: 14.17%
 Beta: 14.22%
 Delta: 14.79%
 Eta: 13.99%
 Gamma: 14.12%
 Kappa: 14.31%
 Zeta: 14.4%


Random Values by Weighted Table
-------------------------------------------------------------------------

population = ('Apple', 'Banana', 'Cherry', 'Grape', 'Lime', 'Orange')
cum_weights = (7, 11, 13, 23, 26, 30)

Cumulative Base Case:
random.choices(pop, cum_weights=cum_weights) x 10000: Total time: 18.756 ms, Average time: 1876 nano
 Apple: 23.48%
 Banana: 13.05%
 Cherry: 6.79%
 Grape: 33.08%
 Lime: 9.93%
 Orange: 13.67%

weights = (7, 4, 2, 10, 3, 4)

Relative Base Case:
random.choices(pop, weights) x 10000: Total time: 21.867 ms, Average time: 2187 nano
 Apple: 23.23%
 Banana: 12.97%
 Cherry: 6.13%
 Grape: 33.65%
 Lime: 10.56%
 Orange: 13.46%

cumulative_table = ((7, 'Apple'), (11, 'Banana'), (13, 'Cherry'), (23, 'Grape'), (26, 'Lime'), (30, 'Orange'))

Fortuna.cumulative_weighted_choice(cumulative_table) x 10000: Total time: 1.675 ms, Average time: 168 nano
 Apple: 23.39%
 Banana: 13.33%
 Cherry: 6.61%
 Grape: 33.56%
 Lime: 10.1%
 Orange: 13.01%

cumulative_choice = CumulativeWeightedChoice(cumulative_table)

cumulative_choice() x 10000: Total time: 2.617 ms, Average time: 262 nano
 Apple: 23.23%
 Banana: 13.58%
 Cherry: 6.72%
 Grape: 33.53%
 Lime: 9.6%
 Orange: 13.34%

relative_table = ((7, 'Apple'), (4, 'Banana'), (2, 'Cherry'), (10, 'Grape'), (3, 'Lime'), (4, 'Orange'))
relative_choice = RelativeWeightedChoice(relative_table)

relative_choice() x 10000: Total time: 2.587 ms, Average time: 259 nano
 Apple: 23.92%
 Banana: 13.36%
 Cherry: 6.5%
 Grape: 32.58%
 Lime: 10.22%
 Orange: 13.42%


Random Values by Category
-------------------------------------------------------------------------

flex_cat = FlexCat(OrderedDict({
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
}), y_bias="front", x_bias="flat")

flex_cat('Cat_A') x 10000: Total time: 2.775 ms, Average time: 277 nano
 A1: 19.77%
 A2: 20.22%
 A3: 20.07%
 A4: 19.64%
 A5: 20.3%

flex_cat('Cat_B') x 10000: Total time: 3.142 ms, Average time: 314 nano
 B1: 19.98%
 B2: 20.01%
 B3: 19.78%
 B4: 20.72%
 B5: 19.51%

flex_cat('Cat_C') x 10000: Total time: 3.172 ms, Average time: 317 nano
 C1: 20.45%
 C2: 20.16%
 C3: 19.97%
 C4: 19.88%
 C5: 19.54%

flex_cat() x 10000: Total time: 4.337 ms, Average time: 434 nano
 A1: 9.84%
 A2: 9.7%
 A3: 10.04%
 A4: 10.22%
 A5: 9.71%
 B1: 6.54%
 B2: 6.8%
 B3: 6.36%
 B4: 7.26%
 B5: 6.7%
 C1: 3.37%
 C2: 3.25%
 C3: 3.58%
 C4: 3.32%
 C5: 3.31%


-------------------------------------------------------------------------
Total Test Time: 0.2 sec

</pre>

## Fortuna Beta Development Log
**Fortuna 0.19.3** \
_Updated plus_or_minus_curve to allow unbounded output._

**Fortuna 0.19.2** \
_Internal development cycle_ \
_Minor update to FlexCat for better debugging._

**Fortuna 0.19.1** \
_Internal development cycle_

**Fortuna 0.19.0** \
_Updated documentation for clarity._ \
_MultiCat has been removed, it is replaced by FlexCat._ \
_Mostly has been removed, it is replaced by QuantumMonty._

**Fortuna 0.18.7** \
_Fixed some more README typos._

**Fortuna 0.18.6** \
_Fixed some README typos._

**Fortuna 0.18.5** \
_Updated documentation._ \
_Fixed another minor test bug._ \

**Fortuna 0.18.4** \
_Updated documentation to reflect recent changes._ \
_Fixed some small test bugs._ \
_Reduced default number of test cycles to 10,000 - down from 100,000._

**Fortuna 0.18.3** \
_Fixed some minor README typos._

**Fortuna 0.18.2** \
_Fixed a bug with Fortuna Pure._

**Fortuna 0.18.1** \
_Fixed some minor typos._ \
_Added tests to Fortuna Pure._

**Fortuna 0.18.0** \
_Introduced new test format, now includes average call time in nanoseconds._ \
_Reduced default number of test cycles to 100,000 - down from 1,000,000._ \
_Added pure Python implementation of Fortuna:_ `.../fortuna_extras/fortuna_pure.py` \
_Promoted several low level functions to top level._
- `zero_flat(num: int) -> int`
- `zero_cool(num: int) -> int`
- `zero_extreme(num: int) -> int`
- `max_cool(num: int) -> int`
- `max_extreme(num: int) -> int`
- `analytic_continuation(func: staticmethod, num: int) -> int`
- `min_max(num: int, lo: int, hi: int) -> int`

**Fortuna 0.17.3** \
_Internal development cycle._

**Fortuna 0.17.2** \
_User Requested: dice() and d() functions now support negative numbers as input._

**Fortuna 0.17.1** \
_Fixed some minor typos._

**Fortuna 0.17.0** \
_Added QuantumMonty to replace Mostly, same default behavior with more options._ \
_Mostly is depreciated and may be removed in a future release._ \
_Added FlexCat to replace MultiCat, same default behavior with more options._ \
_MultiCat is depreciated and may be removed in a future release._ \
_Expanded the Treasure Table example in .../fortuna_extras/fortuna_examples.py_

**Fortuna 0.16.2** \
_Minor refactoring for WeightedChoice_

**Fortuna 0.16.1** \
_Redesigned fortuna_examples.py to feature a dynamic random magic item generator._ \
_Raised cumulative_weighted_choice function to top level._ \
_Added test for cumulative_weighted_choice as free function._ \
_Updated MultiCat documentation for clarity._

**Fortuna 0.16.0** \
_Pushed distribution_timer to the .pyx layer._ \
_Changed default number of iterations of tests to 1 million, up form 1 hundred thousand._ \
_Reordered tests to better match documentation._ \
_Added Base Case Fortuna.fast_rand_below._
_Added Base Case Fortuna.fast_d._ \
_Added Base Case Fortuna.fast_dice._

**Fortuna 0.15.10** \
_Internal Development Cycle_

**Fortuna 0.15.9** \
_Added Base Cases for random.choices_ \
_Added Base Case for randint_dice_

**Fortuna 0.15.8** \
_Clarified MultiCat Test_

**Fortuna 0.15.7** \
_Fixed minor typos._

**Fortuna 0.15.6** \
_Fixed minor typos._ \
_Simplified MultiCat example._

**Fortuna 0.15.5** \
_Added MultiCat test._ \
_Fixed some minor typos in docs._

**Fortuna 0.15.4** \
_Performance optimization for both WeightedChoice() variants._ \
_Cython update provides small performance enhancement across the board._ \
_Compilation now leverages Python3 all the way down._ \
_MultiCat pushed to the .pyx layer for better performance._

**Fortuna 0.15.3** \
_Reworked the MultiCat example to include several randomizing strategies working in concert._ \
_Added Multi Dice 10d10 performance tests._ \
_Updated sudo code in documentation to be more pythonic._

**Fortuna 0.15.2** \
_Fixed: Linux installation failure._ \
_Added: complete source files to the distribution (.cpp .hpp .pyx)._

**Fortuna 0.15.1** \
_Updated & simplified distribution_timer in fortuna_tests.py_ \
_Readme updated, fixed some typos._ \
_Known issue preventing successful installation on some linux platforms._

**Fortuna 0.15.0** \
_Performance tweaks._ \ 
_Readme updated, added some details._

**Fortuna 0.14.1** \
_Readme updated, fixed some typos._

**Fortuna 0.14.0** \
_Fixed a bug where the analytic continuation algorithm caused a rare issue during compilation on some platforms._

**Fortuna 0.13.3** \
_Fixed Test Bug: percent sign was missing in output distributions._ \
_Readme updated: added update history, fixed some typos._

**Fortuna 0.13.2** \
_Readme updated for even more clarity._

**Fortuna 0.13.1** \
_Readme updated for clarity._

**Fortuna 0.13.0** \
_Minor Bug Fixes._ \
_Readme updated for aesthetics._ \
_Added Tests: .../fortuna_extras/fortuna_tests.py_

**Fortuna 0.12.0** \
_Internal test for future update._

**Fortuna 0.11.0** \
_Initial Release: Public Beta_

**Fortuna 0.10.0** \
_Module name changed from Dice to Fortuna_


## Legal Stuff
Fortuna :: Copyright (c) 2018 Broken aka Robert W. Sharp

Permission is hereby granted, free of charge, to any person obtaining a copy \
of this software and associated documentation files (the "Software"), to deal \
in the Software without restriction, including without limitation the rights \
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell \
copies of the Software, and to permit persons to whom the Software is \
furnished to do so, subject to the following conditions:

This README.md file shall be included in all copies or portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR \
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, \
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE \
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER \
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, \
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE \
SOFTWARE.
