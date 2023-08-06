from functools import wraps

def except_this(errors=(Exception, ), default_value="default"):


    def decorator_func(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                print("error func:", func.__name__)
                print("ERROR: ", repr(e))
                return default_value

        return wrapper

    return decorator_func


@except_this()
def example(a):
    b = int(a)
    print(b)
    return b


if __name__ == '__main__':
    example("a")