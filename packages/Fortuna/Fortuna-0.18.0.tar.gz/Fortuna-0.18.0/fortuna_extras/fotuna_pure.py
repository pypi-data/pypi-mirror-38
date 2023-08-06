from collections import OrderedDict
from random import shuffle, randint, randrange, gauss
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
