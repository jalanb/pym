def method(*args):
    pass


a = b = c = 0
method()
method(1, 2)
method(a=1)
method(a, b=1)
method(*a)
method(a, *b)
method(**a)
method(a, **b)
method(a, *b, **c)
