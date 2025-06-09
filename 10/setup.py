''' модуль для capi  '''
from setuptools import setup, Extension


def main():
    '''
    сборка проекта из модуля си
    '''
    setup(
        name="custom_json",
        version="1.0.0",
        ext_modules=[Extension("custom_json", ["custom_json.c"])],
    )

if __name__ == "__main__":
    main()
