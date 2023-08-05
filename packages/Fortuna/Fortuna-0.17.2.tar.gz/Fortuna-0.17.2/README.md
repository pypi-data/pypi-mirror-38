# Fortuna Beta: Fast & Flexible Random Value Generator
#### Adventures in Predictable Non-determinism
More than just a high performance random number generator. 
Fortuna can help you build dynamic rarefied random value generators and more. 
See the Treasure Tables in ...fortuna_extras/fortuna_examples.py

_Fortuna is under active development._

#### Suggested Installation Method:
Open your favorite Unix terminal and type `pip install Fortuna`

## Primary Functions
_Note: All ranges are inclusive unless stated otherwise._

`Fortuna.random_range(lo: int, hi: int) -> int` \
Input argument order is ignored. \
Returns a random integer in range `[lo..hi]` inclusive. \
Up to 15x faster than random.randint(). \
Flat uniform distribution.

`Fortuna.random_below(num: int) -> int` \
Returns a random integer in the exclusive range `[0..num)` for positive values of num. \
This function is analytically continued for input values of less than one. \
This makes the name random_below loose some meaning, random_to_zero may be better. \
Returns a random integer in the exclusive range `(num..0]` for negative values of num. \
This function never returns the value of num except in the case where `num == 0` \
As a result, it will always return zero if num is in range `[-1..1]` \
Flat uniform distribution.

`Fortuna.d(sides: int) -> int` \
Represents a single die roll of a given size die. \
Returns a random integer in the range `[1..sides]` \
Logic suggests the value of sides to be greater than zero. \
Flat uniform distribution.

`Fortuna.dice(rolls: int, sides: int) -> int` \
Returns a random integer in range `[X..Y]` where `X == rolls` and `Y == rolls * sides` \
Logic suggests the values of rolls and sides to be greater than zero. \
Represents the sum of multiple rolls of the same size die. \
Geometric distribution based on the number and size of the dice rolled. \
Complexity scales primarily with the number of rolls, not the size of the dice.

`Fortuna.plus_or_minus(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range `[-num..num]` \
Flat uniform distribution.

`Fortuna.plus_or_minus_linear(num: int) -> int` \
Negative or positive input will produce an equivalent distribution. \
Returns random integer in the range `[-num..num]` \
Zero peak geometric distribution, triangle.

`Fortuna.plus_or_minus_curve(num: int) -> int` \
Negative or positive input will produce an equivalent distributions. \
Returns random integer in the range `[-num..num]` \
Zero centered gaussian distribution, bell curve: Mean = 0, Variance = num / pi

`Fortuna.percent_true(num: int) -> bool` \
Always returns False if num is 0 or less, always returns True if num is 100 or more. \
Any value of num in range `[1..99]` will produce True or False. \
Returns a random Bool based on the probability of True as a percentage.

`Fortuna.random_value(arr: sequence) -> value` \
Returns a random value from a sequence (list or tuple), uniform distribution, non-destructive. \
Up to 10x faster than random.choice()

`Fortuna.cumulative_weighted_choice(table: sequence) -> value` \
Core function for the WeightedChoice base class. \
Produces a custom distribution of values based on cumulative weight. \
Requires input format: `[(weight, value), ... ]` sorted in ascending order by weight. \
Weights must be unique positive integers. \
Up to 15x faster than random.choices()


## Class Abstractions
### Quantum Monty: previously named Mostly
A set of strategies for producing random values from a sequence where the probability \
of each value is based on the monty you choose. For example: the mostly_front monty \
produces random values where the beginning of the sequence is geometrically more common than the back.

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some tiny fraction of the length of the sequence. Method scaling may very slightly.
<pre>
some_sequence = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
quantum_monty = Fortuna.QuantumMonty(some_sequence)
</pre>
`quantum_monty.mostly_front() -> value` \
Returns a random value, mostly from the front of the list (geometric)

`quantum_monty.mostly_middle() -> value` \
Returns a random value, mostly from the middle of the list (geometric)

`quantum_monty.mostly_back() -> value` \
Returns a random value, mostly from the back of the list (geometric)

`quantum_monty.mostly_first() -> value` \
Returns a random value, mostly from the very front of the list (gaussian)

`quantum_monty.mostly_center() -> value` \
Returns a random value, mostly from the very center of the list (gaussian)

`quantum_monty.mostly_last() -> value` \
Returns a random value, mostly from the very back of the list (gaussian)

`quantum_monty.mostly_flat() -> value` \
Returns a random value, (uniform flat)

`quantum_monty.mostly_cycle() -> value` \
Returns a random value, cycles the data with Truffle Shuffle (uniform flat)

`quantum_monty.quantum_monty() -> value` \
Returns a random value, Quantum Monty Algorithm (complex non-uniform)

### Random Cycle: The Truffle Shuffle
Returns a random value from the sequence. Produces a uniform distribution with no consecutive duplicates 
and relatively few nearly consecutive duplicates. Longer sequences will naturally push duplicates even further apart. 
This behavior gives rise to output sequences that seem much less mechanical than other random_value sequences. 

- Constructor takes a copy of a sequence (list or tuple) of arbitrary values.
- Sequence length must be greater than three, best if ten or more.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Features continuous smart micro-shuffling: The Truffle Shuffle.
- Performance scales by some small fraction of the length of the sequence.
<pre>
some_sequence = ["Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta"]
random_cycle = Fortuna.RandomCycle(some_sequence)
random_cycle() -> value
</pre>

### Weighted Choice: Custom Rarity
Two strategies for selecting random values from a sequence where rarity counts. \
Both produce a custom distribution of values based on the weights of the values. \
Up to 10x faster than random.choices()

- Constructor takes a copy of a sequence of weighted value pairs... `[(weight, value), ... ]`
- Automatically optimizes the sequence for correctness and optimal call performance.
- The sequence must not be empty, and each pair must have a weight and a value.
- Weights must be integers. A future release may allow weights to be floats.
- Values can be any Python object that can be passed around... string, int, list, function etc.
- Performance scales by some fraction of the length of the sequence.

The following examples produce equivalent distributions with comparable performance. 
The choice to use one over the other is purely about which strategy suits you or the data best.
Relative weights are easier to understand at a glance, while RPG Treasure Tables map rather nicely to cumulative weights.
Cumulative weights are slightly easier for humans to get wrong, because math. Relative weights can be compared directly
while cumulative weights can not. The tables below have been constructed to have the exact same 
probabilities for each corresponding value.

#### Cumulative Weight Strategy:
Note: Logic dictates Cumulative Weights must be unique!
<pre>
cumulative_weighted_table = (
    (7, "Apple"),
    (11, "Banana"),
    (13, "Cherry"),
    (23, "Grape"),
    (26, "Lime"),
    (30, "Orange"),
)
cumulative_weighted_choice = Fortuna.CumulativeWeightedChoice(cumulative_weighted_table)
cumulative_weighted_choice() -> value
</pre>

#### Relative Weight Strategy:
<pre>
relative_weighted_table = (
    (7, "Apple"),
    (4, "Banana"),
    (2, "Cherry"),
    (10, "Grape"),
    (3, "Lime"),
    (4, "Orange"),
)
relative_weighted_choice = Fortuna.RelativeWeightedChoice(relative_weighted_table)
relative_weighted_choice() -> value
</pre>

### FlexCat, previously named MultiCat
_Controlled Chaos Incarnate_ \
FlexCat wraps an OrderedDict of keyed sequences. \
The Y axis keys are accessed directly, or randomized with one of the QuantumMonty methods (y_bias). \
The X axis sequences are randomized with one of the QuantumMonty methods (x_bias). \
With nine methods across two dimensions... that's 81 configurations.

By default FlexCat will use `y_bias="front"` and `x_bias="cycle"` if not specified at initialization. 
This will make the top of the data structure geometrically more common than the bottom and produces a flat 
cycled distribution for each category. The FlexCat defaults match the original behavior of MultiCat.

Options for x & y bias: _See QuantumMonty for details_
- front, geometric descending
- middle, geometric pyramid
- back, geometric ascending
- first, gaussian descending
- center, gaussian bell curve
- last, gaussian ascending
- flat, uniform flat
- cycle, cycled uniform flat
- monty, Quantum Monty algorithm

<pre>
flex_cat = FlexCat(
    OrderedDict({
        "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
        "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
        "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
    }), y_bias="cycle", x_bias="cycle"
)
flex_cat("Cat_A") -> random value from "Cat_A" : cycled uniform distribution
flex_cat("Cat_B") -> random value from "Cat_B" : cycled uniform distribution
flex_cat("Cat_C") -> random value from "Cat_C" : cycled uniform distribution
flex_cat() -> random value from randomly cycled category : cycled uniform distribution
</pre>


## Fortuna 0.17.2 Sample Distribution and Performance Tests
Testbed: MacOS 10.13.6, Python3.7, Quad 2.7GHz i7 Skylake, 16GB RAM, 1TB SSD
<pre>
$ python3.7 .../fortuna_extras/fortuna_tests.py

Running 1,000,000 cycles of each...


Random Numbers
-------------------------------------------------------------------------

Base Case:
random.randint(1, 10) x 1000000: 1324.53 ms
 1: 10.03%
 2: 10.02%
 3: 9.96%
 4: 10.02%
 5: 9.99%
 6: 9.95%
 7: 10.01%
 8: 10.01%
 9: 10.02%
 10: 10.01%

Fortuna.random_range(1, 10) x 1000000: 80.35 ms
 1: 10.01%
 2: 10.04%
 3: 10.0%
 4: 9.98%
 5: 9.97%
 6: 9.97%
 7: 10.07%
 8: 9.99%
 9: 9.98%
 10: 9.99%

Base Case:
random.randrange(10) x 1000000: 913.81 ms
 0: 10.0%
 1: 9.98%
 2: 9.99%
 3: 9.98%
 4: 9.99%
 5: 10.0%
 6: 10.08%
 7: 10.02%
 8: 10.0%
 9: 9.97%

Fortuna.random_below(10) x 1000000: 77.31 ms
 0: 10.04%
 1: 9.97%
 2: 10.01%
 3: 10.0%
 4: 9.99%
 5: 10.04%
 6: 10.05%
 7: 9.92%
 8: 9.97%
 9: 10.01%

Fortuna.d(10) x 1000000: 77.7 ms
 1: 9.97%
 2: 9.98%
 3: 10.01%
 4: 9.99%
 5: 10.04%
 6: 10.0%
 7: 9.99%
 8: 10.01%
 9: 10.04%
 10: 9.98%

Fortuna.dice(2, 6) x 1000000: 104.22 ms
 2: 2.76%
 3: 5.53%
 4: 8.36%
 5: 11.12%
 6: 13.88%
 7: 16.68%
 8: 13.86%
 9: 11.15%
 10: 8.33%
 11: 5.56%
 12: 2.77%

Fortuna.plus_or_minus(5) x 1000000: 74.5 ms
 -5: 9.12%
 -4: 9.11%
 -3: 9.11%
 -2: 9.09%
 -1: 9.09%
 0: 9.02%
 1: 9.15%
 2: 9.07%
 3: 9.09%
 4: 9.1%
 5: 9.05%

Fortuna.plus_or_minus_linear(5) x 1000000: 102.6 ms
 -5: 2.77%
 -4: 5.55%
 -3: 8.31%
 -2: 11.07%
 -1: 13.9%
 0: 16.63%
 1: 13.94%
 2: 11.15%
 3: 8.31%
 4: 5.57%
 5: 2.79%

Fortuna.plus_or_minus_curve(5) x 1000000: 124.17 ms
 -5: 0.21%
 -4: 1.16%
 -3: 4.43%
 -2: 11.46%
 -1: 20.4%
 0: 24.71%
 1: 20.3%
 2: 11.54%
 3: 4.41%
 4: 1.18%
 5: 0.21%


Random Truth
-------------------------------------------------------------------------

Fortuna.percent_true(25) x 1000000: 73.77 ms
 False: 75.0%
 True: 25.0%


Random Values from a Sequence
-------------------------------------------------------------------------

Base Case:
random.choice(some_list) x 1000000: 738.28 ms
 Alpha: 14.31%
 Beta: 14.28%
 Delta: 14.33%
 Eta: 14.28%
 Gamma: 14.24%
 Kappa: 14.25%
 Zeta: 14.31%

Fortuna.random_value(some_list) x 1000000: 72.52 ms
 Alpha: 14.23%
 Beta: 14.27%
 Delta: 14.34%
 Eta: 14.31%
 Gamma: 14.26%
 Kappa: 14.31%
 Zeta: 14.27%

monty.mostly_front() x 1000000: 210.94 ms
 Alpha: 25.03%
 Beta: 21.42%
 Delta: 17.83%
 Eta: 14.34%
 Gamma: 10.67%
 Kappa: 7.14%
 Zeta: 3.57%

monty.mostly_middle() x 1000000: 164.68 ms
 Alpha: 6.23%
 Beta: 12.49%
 Delta: 18.68%
 Eta: 25.0%
 Gamma: 18.86%
 Kappa: 12.49%
 Zeta: 6.25%

monty.mostly_back() x 1000000: 208.01 ms
 Alpha: 3.56%
 Beta: 7.17%
 Delta: 10.75%
 Eta: 14.33%
 Gamma: 17.86%
 Kappa: 21.38%
 Zeta: 24.95%

monty.mostly_first() x 1000000: 248.74 ms
 Alpha: 34.3%
 Beta: 29.88%
 Delta: 20.06%
 Eta: 10.27%
 Gamma: 4.02%
 Kappa: 1.2%
 Zeta: 0.28%

monty.mostly_center() x 1000000: 196.78 ms
 Alpha: 0.41%
 Beta: 5.36%
 Delta: 24.22%
 Eta: 39.93%
 Gamma: 24.29%
 Kappa: 5.35%
 Zeta: 0.43%

monty.mostly_last() x 1000000: 247.29 ms
 Alpha: 0.27%
 Beta: 1.21%
 Delta: 4.01%
 Eta: 10.33%
 Gamma: 20.05%
 Kappa: 29.94%
 Zeta: 34.19%

monty.mostly_cycle() x 1000000: 635.33 ms
 Alpha: 14.28%
 Beta: 14.29%
 Delta: 14.29%
 Eta: 14.29%
 Gamma: 14.27%
 Kappa: 14.3%
 Zeta: 14.28%

monty.mostly_flat() x 1000000: 143.52 ms
 Alpha: 14.28%
 Beta: 14.27%
 Delta: 14.31%
 Eta: 14.3%
 Gamma: 14.29%
 Kappa: 14.3%
 Zeta: 14.25%

monty.quantum_monty() x 1000000: 318.15 ms
 Alpha: 11.61%
 Beta: 12.86%
 Delta: 15.9%
 Eta: 19.07%
 Gamma: 15.98%
 Kappa: 12.95%
 Zeta: 11.62%

random_cycle() x 1000000: 557.39 ms
 Alpha: 14.28%
 Beta: 14.27%
 Delta: 14.28%
 Eta: 14.29%
 Gamma: 14.28%
 Kappa: 14.28%
 Zeta: 14.32%


Random Values by Weighted Table
-------------------------------------------------------------------------

Cumulative Base Case:
random.choices(pop, cum_weights=cum_weights) x 1000000: 1842.76 ms
 Apple: 23.37%
 Banana: 13.38%
 Cherry: 6.7%
 Grape: 33.28%
 Lime: 9.97%
 Orange: 13.31%

Relative Base Case:
random.choices(pop, weights) x 1000000: 2312.17 ms
 Apple: 23.34%
 Banana: 13.34%
 Cherry: 6.64%
 Grape: 33.33%
 Lime: 10.0%
 Orange: 13.36%

Fortuna.cumulative_weighted_choice(cumulative_table) x 1000000: 172.03 ms
 Apple: 23.35%
 Banana: 13.3%
 Cherry: 6.66%
 Grape: 33.35%
 Lime: 10.05%
 Orange: 13.3%

cumulative_choice() x 1000000: 273.5 ms
 Apple: 23.31%
 Banana: 13.3%
 Cherry: 6.67%
 Grape: 33.41%
 Lime: 9.98%
 Orange: 13.33%

relative_choice() x 1000000: 274.69 ms
 Apple: 23.35%
 Banana: 13.36%
 Cherry: 6.67%
 Grape: 33.31%
 Lime: 10.01%
 Orange: 13.31%


Random Values by Category
-------------------------------------------------------------------------

flex_cat('Cat_A') x 1000000: 280.94 ms
 A1: 19.99%
 A2: 20.01%
 A3: 20.0%
 A4: 19.98%
 A5: 20.03%

flex_cat('Cat_B') x 1000000: 302.29 ms
 B1: 20.02%
 B2: 19.99%
 B3: 20.01%
 B4: 20.01%
 B5: 19.96%

flex_cat('Cat_C') x 1000000: 322.99 ms
 C1: 20.01%
 C2: 19.99%
 C3: 20.05%
 C4: 19.95%
 C5: 20.0%

flex_cat() x 1000000: 434.8 ms
 A1: 10.04%
 A2: 10.01%
 A3: 10.05%
 A4: 9.98%
 A5: 9.99%
 B1: 6.67%
 B2: 6.66%
 B3: 6.68%
 B4: 6.67%
 B5: 6.65%
 C1: 3.32%
 C2: 3.34%
 C3: 3.36%
 C4: 3.26%
 C5: 3.32%


-------------------------------------------------------------------------
Total Test Time: 17.03 sec

</pre>

## Fortuna Beta Development Log
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
