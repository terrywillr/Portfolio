# standard_library.py
"""Python Essentials: The Standard Library.
<Name> William Terry
<Class> Math 341 Section 004
<Date>9/8/20
"""

# Problem 1
def prob1(L):
    return min(L), max(L), sum(L) / len(L)


# Problem 2
def prob2():
    int1 = 0
    int2 = int1
    int2 = 1

    str1 = "happy"
    str2 = str1
    str2 = "sad"

    lst1 = [0, 1, 2]
    lst2 = lst1
    lst2[1] = 0

    tuple1 = ('cat', 'dog', 'apple')
    tuple2 = tuple1
    tuple2 += (1,)

    set1 = {'a', 'b', 'c'}
    set2 = set1
    set2 = set2.add(2)
    print("Int is immutable, Str is immutable, List is mutable, Tuple is immutable, Set is mutable")


# Problem 3
def hypot(a, b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any functions other than those that are imported from your
    'calculator' module.

    Parameters:
        a: the length one of the sides of the triangle.
        b: the length the other non-hypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    import calculator as calc
    #Takes the square root of a^2 added to b^2
    return calc.squarert(calc.sum(calc.mult(a, a), calc.mult(b, b)))


# Problem 4
import itertools

def power_set(A):
    """Use itertools to compute the power set of A.

    Parameters:
        A (iterable): a str, list, set, tuple, or other iterable collection.

    Returns:
        (list(sets)): The power set of A as a list of sets.
    """
    s = list(A)
    power_set = list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1)))
    return [set(s) for s in power_set]



# Problem 5: Implement shut the box.
import sys
import time
import random
def shut_the_box(player, timelimit):
    """Play a single game of shut the box."""
    import box
    remaining = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    start = time.time()
    end = time.time()
    while end - start < int(timelimit):  # Game will end when time is up.
        if max(remaining) < 7:  # Only rolls 1 dice if necessary
            roll = random.randint(1, 6)

        else:
            roll = random.randint(2, 12)
        if box.isvalid(roll, remaining):
            print("Numbers left:", remaining)
            print("Seconds left:", round(int(timelimit) - (end - start), 2))
            print("Roll:", roll)
            player_input = input("Numbers to eliminate:")
            if len(box.parse_input(player_input, remaining)) == 0:  # checks for valid input from player
                print("Invalid input\n")
            # removes player's choice from the remaining numbers
            remaining = [i for i in remaining if i not in box.parse_input(player_input, remaining)]

        if len(remaining) == 0:  # If the player removes all the numbers, they win.
            print("Score for player", sys.argv[1] + ":", sum(remaining))
            print("Time played:", round(end - start, 2), "seconds")
            print("Congratulations!! You shut the box")
            break

        end = time.time()
    if len(remaining) != 0:  # If time runs out and not all numbers are down, player loses
        print("Score for player", sys.argv[1] + ":", sum(remaining), sep=" ")
        print("Time played:", round(end - start, 2), "seconds")
        print("Better luck next time >:)")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        shut_the_box(sys.argv[1], sys.argv[2])
        

