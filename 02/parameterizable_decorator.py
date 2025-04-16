from functools import wraps


def retry_deco(restarts = 1: int, exceptions=None: list = ()):
    if exceptions == None:
        exceptions = []
    if restarts < 1:
        raise ValueError(
            "retries не может быть отрицптельным"
        )
    template = 'Вызов функции: {} с аргументами {} {}. Номер попытки: {}'
    def call_logging(func):
        @wraps(func)
        def catching_errors(*args, **kwargs):
            i = 0
            while i < restarts:
                try:
                    result = func(*args, **kwargs)
                    print(template.format(func.__name__, args, kwargs, i) + f", результат: {result}")
                    return result
                except tuple(exceptions) as e:
                    i += 1
                    print(
                        template.format(func.__name__, args, kwargs, i) +" ошибка: {e}")
                    if i >= restarts:
                        raise e
                except Exception as e:
                    i += 1
                    raise e
            return func(*args, **kwargs)
        return catching_errors
    return call_logging
