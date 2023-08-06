import functools

class Service:
    def __init__(self, name):
        self.name = name
        self.functions = {}

    def handle(self, request):
        print(request.headers, request.data)
        print(self.functions[request.function]("World"))

    def function(self, recieves=None, returns=None, **kwargs):
        def wrapper(func):
            self.functions[func.__name__] = func
            @functools.wraps(func)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return func_wrapper
        return wrapper