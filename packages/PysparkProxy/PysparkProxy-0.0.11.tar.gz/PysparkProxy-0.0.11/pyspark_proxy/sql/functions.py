
class udf(Proxy):
    def __init__(self, f=None):
        self.func = func

        print(func)
        wraps(func)(self)

def udf(f=None):
