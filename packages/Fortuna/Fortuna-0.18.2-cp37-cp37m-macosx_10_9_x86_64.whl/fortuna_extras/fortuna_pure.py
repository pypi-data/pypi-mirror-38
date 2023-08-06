from collections import OrderedDict
from random import shuffle, randint, randrange, gauss, choice, choices
from datetime import datetime


def analytic_continuation(func: staticmethod, num: int) -> int:
    if num < 0:
        return -func(-num)
    elif num == 0:
        return 0
    else:
        return func(num)


def random_range(lo: int, hi: int) -> int:
    return randint(lo, hi)


def random_below(num: int) -> int:
    if num > 0:
        return randrange(0, num)
    else:
        return analytic_continuation(random_below, num)


def d(sides: int) -> int:
    if sides > 0:
        return random_range(1, sides)
    else:
        return analytic_continuation(d, sides)


def dice(rolls: int, sides: int) -> int:
    if rolls > 0:
        return sum(d(sides) for _ in range(rolls))
    elif rolls == 0:
        return 0
    else:
        return -dice(-rolls, sides)


def min_max(num: int, lo: int, hi: int) -> int:
    return min(max(num, lo), hi)


def percent_true(num: int) -> bool:
    return d(100) <= num


def plus_or_minus(num: int) -> int:
    if num > 0:
        return random_range(-num, num)
    else:
        return analytic_continuation(plus_or_minus, num)


def plus_or_minus_linear(num: int) -> int:
    if num > 0:
        return dice(2, num + 1) - (num + 2)
    else:
        return analytic_continuation(plus_or_minus_linear, num)


def plus_or_minus_curve(num: int) -> int:
    if num > 0:
        pi = 3.14159265359
        result = round(gauss(0.0, num / pi))
        while result < -num or result > num:
            result = round(gauss(0.0, num / pi))
        return result
    else:
        return analytic_continuation(plus_or_minus_curve, num)


def zero_flat(num: int) -> int:
    if num > 0:
        return random_range(0, num)
    else:
        return analytic_continuation(zero_flat, num)


def zero_cool(num: int) -> int:
    if num > 0:
        result = plus_or_minus_linear(num)
        while result < 0:
            result = plus_or_minus_linear(num)
        return result
    else:
        return analytic_continuation(zero_cool, num)


def zero_extreme(num: int) -> int:
    if num > 0:
        result = plus_or_minus_curve(num)
        while result < 0:
            result = plus_or_minus_curve(num)
        return result
    else:
        return analytic_continuation(zero_extreme, num)

    
def max_cool(num: int) -> int:
    if num > 0:
        return num - zero_cool(num)
    else:
        return analytic_continuation(max_cool, num)


def max_extreme(num: int) -> int:
    if num > 0:
        return num - zero_extreme(num)
    else:
        return analytic_continuation(max_extreme, num)


def mostly_middle(num: int) -> int:
    if num > 0:
        mid_point = num // 2
        if num % 2 == 0:
            return plus_or_minus_linear(mid_point) + mid_point
        elif percent_true(50):
            return max_cool(mid_point)
        else:
            return 1 + zero_cool(mid_point) + mid_point
    else:
        return analytic_continuation(mostly_middle, num)


def mostly_center(num: int) -> int:
    if num > 0:
        mid_point = num // 2
        if num % 2 == 0:
            return plus_or_minus_curve(mid_point) + mid_point
        elif percent_true(50):
            return max_extreme(mid_point)
        else:
            return 1 + zero_extreme(mid_point) + mid_point
    else:
        return analytic_continuation(mostly_center, num)


def random_value(arr):
    size = len(arr)
    assert size >= 1, f"Input Error, sequence must not be empty."
    return arr[random_below(size)]


def pop_random_value(arr):
    size = len(arr)
    assert size >= 1, f"Input Error, sequence must not be empty."
    return arr.pop(random_below(size))


def cumulative_weighted_choice(table):
    assert len(table) > 0, f"Input Error, sequence must not be empty."
    max_weight = table[-1][0]
    assert max_weight > 0, f"Input Error, the max weight must be greater than 0."
    rand = random_below(max_weight)
    for weight, value in table:
        if weight > rand:
            return value


class RandomCycle:
    """ The Truffle Shuffle """
    __slots__ = ("data", "next", "size", "out_idx", "in_idx")

    def __init__(self, arr):
        self.size = len(arr)
        assert self.size >= 3, f"Input Error, sequence length must be >= 3."
        self.data = list(arr)
        shuffle(self.data)
        self.next = self.data.pop()
        self.out_idx = len(self.data) - 1
        self.in_idx = len(self.data) - 2

    def __call__(self):
        result = self.next
        self.next = self.data.pop(max_extreme(self.out_idx))
        self.data.insert(zero_extreme(self.in_idx), result)
        return result


class QuantumMonty:
    __slots__ = ("data", "max_id", "random_cycle", "dispatch_methods", "monty_methods")

    def __init__(self, data):
        self.data = tuple(data)
        self.max_id = len(data) - 1
        self.random_cycle = RandomCycle(data)
        self.dispatch_methods = {
            "monty": self.quantum_monty,
            "cycle": self.mostly_cycle,
            "front": self.mostly_front,
            "middle": self.mostly_middle,
            "back": self.mostly_back,
            "first": self.mostly_first,
            "center": self.mostly_center,
            "last": self.mostly_last,
            "flat": self.mostly_flat,
        }
        self.monty_methods = (
            self.mostly_front,
            self.mostly_middle,
            self.mostly_back,
            self.mostly_first,
            self.mostly_center,
            self.mostly_last,
        )

    def __call__(self):
        return self.quantum_monty()

    def dispatch(self, quantum_bias="monty"):
        assert quantum_bias in self.dispatch_methods.keys(), "Key Error"
        return self.dispatch_methods[quantum_bias]

    def mostly_flat(self):
        return random_value(self.data)

    def mostly_cycle(self):
        return self.random_cycle()

    def mostly_front(self):
        return self.data[zero_cool(self.max_id)]

    def mostly_back(self):
        return self.data[max_cool(self.max_id)]

    def mostly_middle(self):
        return self.data[mostly_middle(self.max_id)]

    def mostly_first(self):
        return self.data[zero_extreme(self.max_id)]

    def mostly_last(self):
        return self.data[max_extreme(self.max_id)]

    def mostly_center(self):
        return self.data[mostly_center(self.max_id)]

    def quantum_monty(self):
        return random_value(self.monty_methods)()


class WeightedChoice:
    __slots__ = ("data", )

    def __call__(self):
        return cumulative_weighted_choice(self.data)

    @staticmethod
    def _setup(weighted_table, is_cumulative, non_unique=False):
        size = len(weighted_table)
        assert size >= 1, f"Input Error, sequence length must be >= 1."
        if is_cumulative:
            assert size == len(set(w for w, _ in weighted_table)), "Cumulative Weights must be unique, because math."
        if non_unique:
            pass
        else:
            warn_non_unique = (
                "Sanity Check!",
                "  Weighted Values should be unique, pass non_unique=True during instantiation to bypass this check.",
                "  As a result: non-unique values will have their probabilities logically accumulated.",
                "  Relative Weights are summed, Cumulative Weights are over-lapped, but the effect is the same.",
            )
            assert size == len(set(v for _, v in weighted_table)), "\n".join(warn_non_unique)

    @staticmethod
    def _optimize(weighted_table, is_cumulative) -> list:
        if not is_cumulative:
            return sorted([list(itm) for itm in weighted_table], key=lambda x: x[0], reverse=True)
        else:
            data = sorted([list(itm) for itm in weighted_table], key=lambda x: x[0])
            prev_weight = 0
            for w_pair in data:
                w_pair[0], prev_weight = w_pair[0] - prev_weight, w_pair[0]
            return sorted(data, key=lambda x: x[0], reverse=True)

    @staticmethod
    def _package(data) -> tuple:
        cum_weight = 0
        for w_pair in data:
            cum_weight += w_pair[0]
            w_pair[0] = cum_weight
        return tuple(tuple(itm) for itm in data)


class RelativeWeightedChoice(WeightedChoice):

    def __init__(self, weighted_table, non_unique=False):
        self._setup(weighted_table, is_cumulative=False, non_unique=non_unique)
        optimized_data = self._optimize(weighted_table, is_cumulative=False)
        self.data = self._package(optimized_data)


class CumulativeWeightedChoice(WeightedChoice):

    def __init__(self, weighted_table, non_unique=False):
        self._setup(weighted_table, is_cumulative=True, non_unique=non_unique)
        optimized_data = self._optimize(weighted_table, is_cumulative=True)
        self.data = self._package(optimized_data)


class FlexCat:
    __slots__ = ("data_keys", "random_cat", "random_selection")

    def __init__(self, data: OrderedDict, y_bias="front", x_bias="cycle"):
        self.data_keys = tuple(data.keys())
        self.random_cat = QuantumMonty(self.data_keys).dispatch(y_bias)
        self.random_selection = OrderedDict(
            {key: QuantumMonty(sequence).dispatch(x_bias) for key, sequence in data.items()}
        )

    def __call__(self, cat_key=""):
        if not cat_key:
            cat_key = self.random_cat()
        else:
            assert cat_key in self.data_keys, "Key Error"
        return self.random_selection[cat_key]()


def distribution_timer(func: staticmethod, *args, call_sig=None, max_distribution=25, num_cycles=100000, **kwargs):
    start_time = datetime.now()
    results = [func(*args, **kwargs) for _ in range(num_cycles)]
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    if call_sig:
        pass
    elif hasattr(func, "__qualname__"):
        if len(args) == 1:
            call_sig = f"{func.__qualname__}({args[0]})"
        else:
            call_sig = f"{func.__qualname__}{args}"
    else:
        call_sig = f"function(*args, **kwargs)"
    total_time_ms = round(total_time * 1000.0, 2)
    average_time_nano = round((total_time_ms / num_cycles) * 1000000, 2)
    print(f"{call_sig} x {num_cycles}: Total time: {total_time_ms} ms, Average time: {average_time_nano} nano")
    if type(results[0]) is list:
        for i, _ in enumerate(results):
            results[i] = results[i][0]
    unique_results = set(results)
    if len(unique_results) <= max_distribution:
        result_obj = {
            key: f"{round(results.count(key) / (num_cycles / 100), 2)}%" for key in sorted(list(unique_results))
        }
        for key, val in result_obj.items():
            print(f" {key}: {val}")
    print("")


Mostly = QuantumMonty
MultiCat = FlexCat


if __name__ == "__main__":
    t0 = datetime.now()
    print("Fortuna Pure 0.18.2 Sample Distribution and Performance Test Suite\n")
    print("Random Numbers")
    print(f"{'-' * 73}\n")
    distribution_timer(randint, 1, 10, call_sig="Base Case:\nrandom.randint(1, 10)")
    distribution_timer(random_range, 1, 10)
    distribution_timer(randrange, 10, call_sig="Base Case:\nrandom.randrange(10)")
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
    distribution_timer(choice, some_list, call_sig="Base Case:\nrandom.choice(some_list)")
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
        choices, population, cum_weights=cum_weights,
        call_sig="Cumulative Base Case:\nrandom.choices(pop, cum_weights=cum_weights)"
    )
    weights = (7, 4, 2, 10, 3, 4)
    print(f"weights = {weights}\n")
    distribution_timer(
        choices, population, weights,
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
