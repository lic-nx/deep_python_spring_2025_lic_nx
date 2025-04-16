from functools import wraps


def retry_deco(restarts: int, exceptions: list = ()):
    def call_logging(func):
        @wraps(func)
        def catching_errors(*args, **kwargs):
            i = 0
            while i < restarts:
                try:
                    return func(*args, **kwargs)
                except tuple(exceptions) as e:
                    i += 1
                    print(
                        f"Вызов функции: {func.__name__} с аргументами \
{args, kwargs} номер попытки: {i}, ошибка: {e}"
                    )
                    if i >= restarts:
                        raise e
                except Exception as e:
                    i += 1
                    raise e
                else:
                    print(
                        f"Вызов функции: {func.__name__} с аргументами \
{args, kwargs} номер попытки: {i}"
                    )
                    break
            return func(*args, **kwargs)
        return catching_errors
    return call_logging
