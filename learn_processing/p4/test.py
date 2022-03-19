#!/usr/bin/python3

d = {"a": 1, 'b': 2}
for key in d:
    print(key)

print(d)


class Student:
    """explame
    __init__
    expale"""

    def __init__(self) -> None:
        self.age = 18

    def say(self):
        """say a method
        """
        print("da")


std = Student()
print(std.age)