from pdum.coiled.foo import bar

def baz_function():
    return bar() + " from baz"

if __name__ == "__main__":
    print(baz_function())