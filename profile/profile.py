from functools import wraps
import time

def in_profile(input):
    @wraps(input)
    def wrapper(*args, **kwargs):
        print(input.__name__ + ' started')
        start = time.time()
        result = input(*args, **kwargs)
        stop = time.time()
        total = stop - start
        print(input.__name__ + ' finished in {0}s'.format(round(total, 3)))
        return result
    return wrapper

def out_profile(input):
    if isinstance(input, type):
        for name in dir(input):
            if not name.startswith('__') or name == '__init__':
                attr = getattr(input, name)
                setattr(input, name, out_profile(attr))
        return input
    return in_profile(input)

@out_profile
def test(*args, **kwargs):
    time.sleep(1)

@out_profile
class TestClass:
    def __init__(self):
        time.sleep(1)

    def test_class_func(self):
        time.sleep(0.05)


if __name__ == '__main__':
    test1 = TestClass()
    test1.test_class_func()
    test()