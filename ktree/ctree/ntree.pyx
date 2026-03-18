
def hello(name):
    print(f"Hola {name}, desde Cython!")

def fib(int n):
    cdef int i
    cdef double a=0, b=1

    for i in range(n):
        a, b = b, a + b

    return a
