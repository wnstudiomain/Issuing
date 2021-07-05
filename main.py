# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from decimal import Decimal


class StdClass:
    pass


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    number = Decimal("0.1")
    number = number + number + number
    print(number)
    data = StdClass()
    data.mti = "0100"
    data.de002 = "4785292505858379"
    print(data.__dict__)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
