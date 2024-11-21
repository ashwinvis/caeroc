"""
Decorators for formulae classes

"""

from functools import wraps


def storeresult(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = func.__name__
        result = func(self, *args, **kwargs)
        if "store" in kwargs.keys():
            if kwargs["store"] is True:
                self.store(key, result)
        else:
            for arg in args:
                if type(arg) is bool and arg is True:
                    self.store(key, result)

        return result

    return wrapper
