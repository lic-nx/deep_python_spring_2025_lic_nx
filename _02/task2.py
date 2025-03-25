### 2. Параметризуемый декоратор для логирования вызовов и перезапуска функций в случае ошибок
# Декоратор `retry_deco` должен:
# - принимать опциональными параметрами число перезапусков декорируемой функции и список ожидаемых классов исключений;
# - при вызове функции логировать (выводить) название функции, все переданные ей аргументы, номер попытки перезапуска, результат работы функции и ошибку, если было выброшено исключение;
#   формат логирования произвольный (например, функция и аргументы один раз, а номер попытки и исключение/результат сколько потребуется);
# - в случае исключения при выполнении функции декоратор должен выполнить новую попытку запуска функции, пока не достигнет заданного числа перезапусков;
#   если исключение из списка ожидаемых классов исключений (параметр декоратора), то перезапускать функцию не надо, тк исключения из списка это нормальный режим работы декорируемой функции.

# ```py
def retry_deco(restarts:int, exceptions:list=()):
    
    def call_logging(func):
        i = 0
        while i < restarts:
            try:
                def catching_errors(*args, **kwargs):
                    return func(*args, **kwargs)
                return catching_errors
            except exceptions as e:
                i+=1
            else:
                break
    return call_logging



# @retry_deco(3)
# def add(a, b):
#     return a + b


# add(4, 2)
# # run "add" with positional args = (4, 2), attempt = 1, result = 6

# add(4, b=3)
# # run "add" with positional args = (4,), keyword kwargs = {"b": 3}, attempt = 1, result = 7


# @retry_deco(3)
# def check_str(value=None):
#     if value is None:
#         raise ValueError()

#     return isinstance(value, str)


# check_str(value="123")
# # run "check_str" with keyword kwargs = {"value": "123"}, attempt = 1, result = True

# check_str(value=1)
# # run "check_str" with keyword kwargs = {"value": 1}, attempt = 1, result = False

# check_str(value=None)
# # run "check_str" with keyword kwargs = {"value": None}, attempt = 1, exception = ValueError
# # run "check_str" with keyword kwargs = {"value": None}, attempt = 2, exception = ValueError
# # run "check_str" with keyword kwargs = {"value": None}, attempt = 3, exception = ValueError


# @retry_deco(2, [ValueError])
# def check_int(value=None):
#     if value is None:
#         raise ValueError()

#     return isinstance(value, int)

# check_int(value=1)
# # run "check_int" with keyword kwargs = {"value": 1}, attempt = 1, result = True

# check_int(value=None)
# # run "check_int" with keyword kwargs = {"value": None}, attempt = 1, exception = ValueError # нет перезапуска

# ```