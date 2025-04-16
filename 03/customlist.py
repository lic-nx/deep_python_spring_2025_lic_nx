from itertools import zip_longest


class CustomList(list):
    def __eq__(self, value):
        return sum(self) == sum(value)

    def __ne__(self, value):
        return sum(self) != sum(value)

    def __gt__(self, value):
        return sum(self) > sum(value)

    def __lt__(self, value):
        return sum(self) < sum(value)

    def __ge__(self, value):
        return sum(self) >= sum(value)

    def __le__(self, value):
        return sum(self) <= sum(value)

    def __str__(self):
        return f"CustomList({super().__str__()}), Sum: {sum(self)}"

    def __sub__(self, other):
        if isinstance(other, (list, CustomList)):
            res = CustomList([a - b for a, b in
                              zip_longest(self, other, fillvalue=0)])
            return res
        if isinstance(other, int):
            return CustomList([i - other for i in self])
        raise ValueError("sub with this data type is not supported.")

    def __rsub__(self, other):
        if isinstance(other, (list, CustomList)):
            res = CustomList([a - b for a, b in
                              zip_longest(other, self, fillvalue=0)])
            return res
        if isinstance(other, int):
            return CustomList([other - i for i in self])
        raise ValueError("sub with this data type is not supported.")

    def __add__(self, other):
        if isinstance(other, (list, CustomList)):
            res = CustomList([a + b for a, b
                              in zip_longest(self, other, fillvalue=0)])
            return res
        if isinstance(other, int):
            return CustomList(i + other for i in self)
        raise ValueError("summ with this data type is not supported.")

    def __radd__(self, other):
        return self.__add__(other)
