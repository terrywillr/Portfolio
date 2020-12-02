# exceptions_fileIO.py
"""Python Essentials: Exceptions and File Input/Output.
<Name>
<Class>
<Date>
"""

from random import choice


# Problem 1
def arithmagic():
    """
    Takes in user input to perform a magic trick and prints the result.
    Verifies the user's input at each step and raises a
    ValueError with an informative error message if any of the following occur:
    
    The first number step_1 is not a 3-digit number.
    The first number's first and last digits differ by less than $2$.
    The second number step_2 is not the reverse of the first number.
    The third number step_3 is not the positive difference of the first two numbers.
    The fourth number step_4 is not the reverse of the third number.
    """
    
    step_1 = input("Enter a 3-digit number where the first and last "
                                           "digits differ by 2 or more: ")
    if int(step_1) < 100 or int(step_1) > 999:
        raise ValueError("Number must be a 3 digit number")

    elif abs(int(str(step_1)[0]) - int(str(step_1)[2])) < 2:
        raise ValueError("First and last digit of number differ by less than 2")

    step_2 = input("Enter the reverse of the first number, obtained "
                                              "by reading it backwards: ")
    if int(step_2) != int(str(step_1)[::-1]):
        raise ValueError("step_2 is not the reverse of step_1")

    step_3 = input("Enter the positive difference of these numbers: ")

    if int(step_3) != abs(int(step_2) - int(step_1)):
        raise ValueError("step_3 is not the positive difference of step_1, step_2")

    step_4 = input("Enter the reverse of the previous result: ")

    if int(step_4) != int(str(step_3)[::-1]):
        raise ValueError("step_4 is not the reverse of step_3")

    print(str(step_3), "+", str(step_4), "= 1089 (ta-da!)")


# Problem 2
def random_walk(max_iters=1e12):
    """
    If the user raises a KeyboardInterrupt by pressing ctrl+c while the 
    program is running, the function should catch the exception and 
    print "Process interrupted at iteration $i$".
    If no KeyboardInterrupt is raised, print "Process completed".

    Return walk.
    """
    try:
        walk = 0
        directions = [1, -1]
        for i in range(int(max_iters)):
            walk += choice(directions)
    except:
        print("Process interrupted at iteration", i)
    else:
        print("Process completed")
    return walk


# Problems 3 and 4: Write a 'ContentFilter' class.
    """Class for reading in file
        
    Attributes:
        filename (str): The name of the file
        contents (str): the contents of the file
        
    """
class ContentFilter(object):   
    # Problem 3
    def __init__(self, filename):
        """Read from the specified file. If the filename is invalid, prompt
        the user until a valid filename is given.
        """
        self.filename = filename
        self.contents = ""
        correct_file = False
        while not correct_file:
            try:
                infile = open(self.filename, 'r')
                self.contents = infile.read()
                self.numchars = str(sum(len(s) for s in self.contents))
                self.numalpha = str(sum(s.isalpha() for s in (line for line in self.contents)))
                self.numdigit = str(sum(s.isdigit() for s in (line for line in self.contents)))
                self.numwhitespace = str(sum(s.isspace() for s in self.contents))
                self.numlines = str(sum(s.count('\n') for s in self.contents))
                infile.close()
            except (FileNotFoundError, TypeError, OSError) as error:
                print("Invalid file name. Enter another file name.")
                self.filename = input("Enter the name of the file you wish to open: ")
                correct_file = False
            else:
                correct_file = True


    
 # Problem 4 ---------------------------------------------------------------
    def check_mode(self, mode):
        """Raise a ValueError if the mode is invalid."""
        if mode != 'w' or 'x' or 'a':
            raise ValueError("Invalid file access mode. Select either 'w' or 'x' or 'a'")

    def uniform(self, outfile, mode='w', case='upper'):
        """Write the data ot the outfile in uniform case."""
        if case == 'upper':
            with open(outfile, mode) as outfile:
                outfile.write("".join(self.contents).upper())
        elif case == 'lower':
            with open(outfile, mode) as outfile:
                outfile.write("".join(self.contents).lower())
        else:
            raise ValueError("Case is not upper nor lower")


    def reverse(self, outfile, mode='w', unit='word'):
        """Write the data to the outfile in reverse order."""
        if unit == 'line':
            with open(outfile, mode) as outfile:
                outfile.write("".join('\n'.join(self.contents.split('\n')[::-1])).rstrip())
        elif unit == 'word':
            with open(outfile, mode) as outfile:
                outfile.write("".join('\n'.join(line[::-1] for line in self.contents.split('\n'))).rstrip())
        else:
            raise ValueError("Invalid input for unit. Enter 'line' or word'")

    def transpose(self, outfile, mode='w'):
        elements =  "".join(self.contents.split(" ")).split('\n')
        elements.pop()
        print(elements)
        with open(outfile, mode) as outfile:
            for s in zip(*elements):
                outfile.write(''.join(list(s)) + '\n')

    def __str__(self):
        """String representation: info about the contents of the file."""
        return ("Source file:\t\t" + self.filename +
                '\nTotal Characters:\t' + self.numchars +
                "\nAlphabetic characters:\t" + self.numalpha +
                "\nNumerical characters:\t" + self.numdigit +
                '\nWhitespace characters:\t' + self.numwhitespace +
                '\nNumber of Lines:\t' + self.numlines)

"""def test_prob4():
    cf = ContentFilter("cf_example1.txt")
    cf.uniform("uniform.txt", mode='w', case="upper")
    cf.uniform("uniform.txt", mode='a', case="lower")
    cf.reverse("reverse.txt", mode='w', unit="word")
    cf.reverse("reverse.txt", mode='a', unit="line")
    cf.transpose("transpose.txt", mode='w')


if __name__ == "__main__":
    print(ContentFilter(100))"""
