class CustomMeta(type):
    @staticmethod
    def custom_setattr(clas, attr_name, attr_value):
        object.__setattr__(
            clas,
            (
                attr_name
                if attr_name.startswith("__")
                and attr_name.endswith("__")
                and callable(attr_name)
                else f"custom_{attr_name}"
            ),
            attr_value,
        )

    def __new__(mcs, name, bases, dct, **kwargs):
        dct = {
            (
                f"custom_{key}"
                if not key.startswith("__")
                and not key.endswith("__")
                and not callable(key)
                else key
            ): value
            for key, value in dct.items()
        }
        dct["__setattr__"] = CustomMeta.custom_setattr
        return super().__new__(mcs, name, bases, dct, **kwargs)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
