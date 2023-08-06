from Fortuna import *  # from fortuna_extras.fortuna_pure import *
from datetime import datetime
from collections import OrderedDict
import random  # Base Cases - for comparison only


if __name__ == "__main__":
    t0 = datetime.now()
    print("Fortuna 0.18.2 Sample Distribution and Performance Test Suite\n")
    print("Random Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(random.randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    distribution_timer(random_range, 1, 10)
    distribution_timer(random.randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
    distribution_timer(random_below, 10)
    distribution_timer(d, 10)
    distribution_timer(dice, 2, 6)
    distribution_timer(plus_or_minus, 5)
    distribution_timer(plus_or_minus_linear, 5)
    distribution_timer(plus_or_minus_curve, 5)
    distribution_timer(zero_flat, 10)
    distribution_timer(zero_cool, 10)
    distribution_timer(zero_extreme, 10)
    distribution_timer(max_cool, 10)
    distribution_timer(max_extreme, 10)
    distribution_timer(mostly_middle, 10)
    distribution_timer(mostly_center, 10)
    print("")
    print("Random Truth")
    print(f"{'-' * 73}\n")
    distribution_timer(percent_true, 25)
    print("")
    print("Random Values from a Sequence")
    print(f"{'-' * 73}\n")
    some_list = ("Alpha", "Beta", "Delta", "Eta", "Gamma", "Kappa", "Zeta")
    print(f"some_list = {some_list}\n")
    distribution_timer(random.choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
    distribution_timer(random_value, some_list, call_sig="random_value(some_list)")
    monty = QuantumMonty(some_list)
    print("monty = QuantumMonty(some_list)\n")
    distribution_timer(monty.mostly_front, call_sig="monty.mostly_front()")
    distribution_timer(monty.mostly_middle, call_sig="monty.mostly_middle()")
    distribution_timer(monty.mostly_back, call_sig="monty.mostly_back()")
    distribution_timer(monty.mostly_first, call_sig="monty.mostly_first()")
    distribution_timer(monty.mostly_center, call_sig="monty.mostly_center()")
    distribution_timer(monty.mostly_last, call_sig="monty.mostly_last()")
    distribution_timer(monty.mostly_cycle, call_sig="monty.mostly_cycle()")
    distribution_timer(monty.mostly_flat, call_sig="monty.mostly_flat()")
    distribution_timer(monty.quantum_monty, call_sig="monty.quantum_monty()")
    random_cycle = RandomCycle(some_list)
    print("random_cycle = RandomCycle(some_list)\n")
    distribution_timer(random_cycle, call_sig="random_cycle()")
    print("")
    print("Random Values by Weighted Table")
    print(f"{'-' * 73}\n")
    population = ("Apple", "Banana", "Cherry", "Grape", "Lime", "Orange")
    cum_weights = (7, 11, 13, 23, 26, 30)
    print(f"population = {population}\n"
          f"cum_weights = {cum_weights}\n")
    distribution_timer(
        random.choices, population, cum_weights=cum_weights,
        call_sig="Cumulative Base Case:\nrandom.choices(pop, cum_weights=cum_weights)"
    )
    weights = (7, 4, 2, 10, 3, 4)
    print(f"weights = {weights}\n")
    distribution_timer(
        random.choices, population, weights,
        call_sig="Relative Base Case:\nrandom.choices(pop, weights)"
    )
    cumulative_table = (
        (7, "Apple"),
        (11, "Banana"),
        (13, "Cherry"),
        (23, "Grape"),
        (26, "Lime"),
        (30, "Orange"),
    )
    print(f"cumulative_table = {cumulative_table}\n")
    distribution_timer(
        cumulative_weighted_choice, cumulative_table,
        call_sig="Fortuna.cumulative_weighted_choice(cumulative_table)"
    )
    cumulative_choice = CumulativeWeightedChoice(cumulative_table)
    print("cumulative_choice = CumulativeWeightedChoice(cumulative_table)\n")
    distribution_timer(cumulative_choice, call_sig="cumulative_choice()")
    relative_table = (
        (7, "Apple"),
        (4, "Banana"),
        (2, "Cherry"),
        (10, "Grape"),
        (3, "Lime"),
        (4, "Orange"),
    )
    print(f"relative_table = {relative_table}")
    relative_choice = RelativeWeightedChoice(relative_table)
    print("relative_choice = RelativeWeightedChoice(relative_table)\n")
    distribution_timer(relative_choice, call_sig="relative_choice()")
    print("")
    print("Random Values by Category")
    print(f"{'-' * 73}\n")
    flex_cat = FlexCat(OrderedDict({
        "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
        "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
        "Cat_C": ("C1", "C2", "C3", "C4", "C5"),
    }), y_bias="front", x_bias="flat")
    print("""flex_cat = FlexCat(OrderedDict({
    "Cat_A": ("A1", "A2", "A3", "A4", "A5"),
    "Cat_B": ("B1", "B2", "B3", "B4", "B5"),
    "Cat_C": ("C1", "C2", "C3", "C4", "C5"),\n}), y_bias="front", x_bias="flat")\n""")
    distribution_timer(flex_cat, 'Cat_A', call_sig="flex_cat('Cat_A')")
    distribution_timer(flex_cat, 'Cat_B', call_sig="flex_cat('Cat_B')")
    distribution_timer(flex_cat, 'Cat_C', call_sig="flex_cat('Cat_C')")
    distribution_timer(flex_cat, call_sig="flex_cat()")
    print("")
    print(f"{'-' * 73}")
    total_test_time = round((datetime.now() - t0).total_seconds(), 2)
    print(f"Total Test Time: {total_test_time} sec\n")
