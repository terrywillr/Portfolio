# object_oriented.py
"""Python Essentials: Object Oriented Programming.
<Name> William Terry
<Class> Math 345
<Date>9.15.20
"""


class Backpack:
    """A Backpack object class. Has a name and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        contents (list): the contents of the backpack.
        color (str): color of the backpack
        max_size (int): most amount of items backpack can hold.
    """

    # Problem 1: Modify __init__() and put(), and write dump().
    def __init__(self, name, color, max_size = 5):
        """Set the name, color, max size and initialize an empty list of contents.

        Parameters:
            name (str): the name of the backpack's owner.
            color (str): color of the backpack.
            max_size (int): amount of items backpack can hold.
        """
        self.name = name
        self.contents = []
        self.color = color
        self.max_size = max_size


    def put(self, item):
        """Add an item to the backpack's list of contents if there is room."""
        if len(self.contents) < self.max_size:
            self.contents.append(item)

        else:
            print("No Room!")

    def take(self, item):
        """Remove an item from the backpack's list of contents."""
        self.contents.remove(item)

    def dump(self):
        """Remove all items from the backpack's content list."""
        self.contents.clear()



    # Magic Methods -----------------------------------------------------------

    # Problem 3: Write __eq__() and __str__().
    def __add__(self, other):
        """Add the number of contents of each Backpack."""
        return len(self.contents) + len(other.contents)

    def __lt__(self, other):
        """Compare two backpacks. If 'self' has fewer contents
        than 'other', return True. Otherwise, return False.
        """
        return len(self.contents) < len(other.contents)

    def __eq__(self, other):
        """Compare two backpacks. If 'self' has the same name, color, and
        number of contents as 'other', return True. Otherwise, return False."""
        return (self.name == other.name) and (self.color == other.color) and (len(self.contents) == len(other.contents))

    def __str__(self):
       return "Name:\t\t" + self.name + "\n" + "Color:\t\t" + self.color + "\nSize:\t\t" + str(len(self.contents)) + "\nMax Size:\t" + str(self.max_size) +"\nContents:\t" + str(self.contents)


# An example of inheritance. You are not required to modify this class.
class Knapsack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit inside.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """
    def __init__(self, name, color):
        """Use the Backpack constructor to initialize the name, color,
        and max_size attributes. A knapsack only holds 3 item by default.

        Parameters:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit inside.
        """
        Backpack.__init__(self, name, color, max_size=3)
        self.closed = True

    def put(self, item):
        """If the knapsack is untied, use the Backpack.put() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.put(self, item)

    def take(self, item):
        """If the knapsack is untied, use the Backpack.take() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.take(self, item)

    def weight(self):
        """Calculate the weight of the knapsack by counting the length of the
        string representations of each item in the contents list.
        """
        return sum(len(str(item)) for item in self.contents)


# Problem 2: Write a 'Jetpack' class that inherits from the 'Backpack' class.
class Jetpack(Backpack):
    """Jetpack object class. Inherits from Backpack class."""
    """Attributes:
        name (str): name of the jetpack
        color (str): color of the jetpack
        max_size (int): amount of items jackpack and hold
        amount_fuel (int): The amount of fuel in the jetpack"""
    def __init__(self, name, color, max_size = 2, amount_fuel = 10):
        """Parameters:
                name: name of jetpack owner
                color: color of jetpack
                max_size: amount of items jetpack can hold.
                amount_fuel: fuel available in jetpack."""
        Backpack.__init__(self, name, color, max_size)
        self.amount_fuel = amount_fuel

    def fly(self, fuel):
        """Accepts amount of fuel to be burned, and decrements the amount_fuel attribute
        if the user has available fuel to burn"""
        if fuel > self.amount_fuel:
            print("Not enough fuel!")

        else:
            self.amount_fuel -= fuel

    def dump(self):
        """Overrides dump() function in backpack to also dump out fuel as well as contents"""
        Backpack.dump(self)
        self.amount_fuel = 0

def test_backpack():
    testpack = Backpack("Barry", "black", 4)
    if testpack.name != "Barry" or testpack.color != "black":
        print("Backpack.name and color not assigned")

    for item in ["pencil", "pen", "paper", "computer", "textbook", "laptop"]:
        testpack.put(item)

    otherpack = Backpack("Barry", "black", 4)
    for item in ["pencil", "pen", "paper", "computer", "textbook", "laptop"]:
        otherpack.put(item)

    print(testpack == otherpack)
    print(testpack + otherpack)
    print(str(testpack))

def test_jetpack():
    testpack = Jetpack("Will", "Green", 1, 5)
    print (testpack.name, testpack.color, testpack.max_size, testpack.amount_fuel)
    for item in ["Pencil", "Paper", "Scissors", "irradiated materials"]:
        testpack.put(item)
    testpack.fly(4)
    print(testpack.contents, testpack.amount_fuel)
    testpack.dump()
    print(testpack.contents, testpack.amount_fuel)



# Problem 4: Write a 'ComplexNumber' class.
from math import sqrt
class ComplexNumber:
    """Attributes:
    real: the real part of the complex number.
    imag: the imaginary part of the complex number."""
    def __init__(self, real, imag):
        """Parameters:
        real: gives the real part of the complex number
        imag: gives the imaginary part of the complex number"""
        self.real = real
        self.imag = imag

    def conjugate(self):
        "Returns the complex number with the imaginary part negated"
        return ComplexNumber(self.real, -self.imag)

    def __str__(self):
        "Prints the complex number in the form of (a+bj) or (a-bj)"
        if self.imag >= 0:
            return "(" + str(self.real) + "+" + str(self.imag) +"j)"
        else:
            return "(" + str(self.real) + str(self.imag) +"j)"

    def __abs__(self):
        "Returns the magnitude of the complex number"
        return sqrt((self.real * self.real + self.imag * self.imag))

    def __eq__(self, other):
        "If the real and imaginary parts of 2 complex numbers are equal, return True"
        return self.imag == other.imag and self.real == other.real

    def __add__(self, other):
        "Adds the real and imaginary parts of 2 complex numbers together."
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        "Subtracts the real and imaginary parts of the 2 complex numbers together"
        return ComplexNumber(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        "Performs FOIL multiplication on 2 complex numbers."
        return ComplexNumber((self.real * self.real) - (self.imag * other.imag), (self.real * other.imag) + (self.imag * other.real))

    def __truediv__(self, other):
        """Multiplies the numerator and denominator by the conjugate of the denominator
        and returns the resulting complex number."""
        denominator = other * other.conjugate()
        denominator_real = denominator.real
        numerator = self * other.conjugate()
        return ComplexNumber(numerator.real / denominator_real, numerator.imag / denominator_real)


def testcomplex(a, b):
    py_cnum, my_cnum = complex(a,b), ComplexNumber(a,b)
    other_cnum = ComplexNumber(a, b)
    if my_cnum.real != a or my_cnum.imag !=b:
        print("__init__() set self.real and self.imag incorrectly")

    if str(py_cnum) != str(my_cnum):
        print("__str__() failed for", py_cnum)

    if abs(py_cnum) != abs(my_cnum):
        print("__abs__() failed for", py_cnum)

    if my_cnum != other_cnum:
        print("__eq__() failed for", my_cnum)

    if my_cnum + my_cnum != py_cnum + py_cnum:
        print("__add__() failed for", py_cnum)

    if my_cnum - my_cnum != py_cnum - py_cnum:
        print("__sub__() failed for", py_cnum)

    if my_cnum * my_cnum != py_cnum * py_cnum:
        print("__mul__() failed for", py_cnum)

    if my_cnum / my_cnum != py_cnum / py_cnum:
        print("__truediv__() failed for", py_cnum)


    print(my_cnum * my_cnum.conjugate())



#testcomplex(123, 43)
