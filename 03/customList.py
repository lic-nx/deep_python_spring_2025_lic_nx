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
            res = [a - b for a, b, in zip(self, other)]
            res.extend(
                self[len(other):]
                if len(self) > len(other)
                else [-i for i in other[len(self):]]
            )
            return res
        if isinstance(other, int):
            return CustomList([i - other for i in self])
        raise ("sub  with this data type is not supported.")

    def __rsub__(self, other):
        if isinstance(other, (list, CustomList)):
            res = [a - b for a, b, in zip(other, self)]
            res.extend(
                self[len(other):]
                if len(self) > len(other)
                else other[len(self):]
            )
            return res
        if isinstance(other, int):
            return CustomList([other - i for i in self])
        raise ("sub  with this data type is not supported.")

    def __add__(self, other):
        if isinstance(other, (list, CustomList)):
            res = [a + b for a, b, in zip(self, other)]
            res.extend(
                self[len(other):]
                if len(self) > len(other)
                else other[len(self):]
            )
            return res
        if isinstance(other, int):
            return CustomList([i + other for i in self])
        raise("sub  with this data type is not supported.")

    def __radd__(self, other):
        return self.__add__(other)
