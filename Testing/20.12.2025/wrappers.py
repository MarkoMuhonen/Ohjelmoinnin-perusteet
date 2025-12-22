
def safe_call(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Virhe: {e}")
            return None
    return wrapper

@safe_call
def divide(a, b):
    return a / b

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # Virhe: division by zero



def log_wrapper(func):
    def wrapper(*args, **kwargs):
        print(f"Kutsutaan {func.__name__} args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"Tulos: {result}")
        return result
    return wrapper

@log_wrapper
def add(a, b):
    return a + b

add(3, 4)
add(a=5, b=7)



def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Ennen funktiota")
        result = func(*args, **kwargs)
        print("Jälkeen funktion")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hei!")

say_hello()


