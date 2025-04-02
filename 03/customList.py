class CustomList(list):
    def __eq__(self, value):
        return sum(self) == sum(value)
    

# print(help(list))

