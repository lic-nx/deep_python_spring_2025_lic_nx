from functools import wraps


def retry_deco(restarts: int = 1, exceptions: list = None):
    if exceptions is None:
        exceptions = (Exception,)
    elif isinstance(exceptions, type) and issubclass(exceptions, BaseException):
        exceptions = (exceptions,)
    elif isinstance(exceptions, tuple):
        for exc in exceptions:
            if not (isinstance(exc, type) and issubclass(exc, BaseException)):
                raise TypeError(f"Некорректный тип исключения: {exc}")
    else:
        raise TypeError("Параметр 'exceptions' может быть классом исключения или их исключением")

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
                    print(template.format(func.__name__, args,
                                          kwargs, i) + f", результат: {result}")
                    return result
                except exceptions as e:
                    i += 1
                    print(
                        template.format(func.__name__, args,
                                        kwargs, i) + " ошибка: {e}")
                    if i >= restarts:
                        raise e
                except Exception as e:
                    i += 1
                    raise e
            return func(*args, **kwargs)
        return catching_errors
    return call_logging
