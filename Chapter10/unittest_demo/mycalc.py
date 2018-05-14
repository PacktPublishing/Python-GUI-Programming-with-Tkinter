import random

class MyCalc:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add(self):
        return self.a + self.b

    def mod_divide(self):
        if self.b == 0:
            raise ValueError("Cannot divide by zero")
        return (int(self.a / self.b), self.a % self.b)

    def mod_divide2(self):
        if type(self.a) is not int or type(self.b) is not int:
            raise ValueError("Method only valid for ints")
        if self.b == 0:
            raise ValueError("Cannot divide by zero")
        return (self.a // self.b, self.a % self.b)

    def rand_between(self):
        return (
            (random.random() * abs(self.a - self.b)) +
            min(self.a, self.b))
