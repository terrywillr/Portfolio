# regular_expressions.py
"""Volume 3: Regular Expressions.
<Name>
<Class>
<Date>
"""
import re

# Problem 1
def prob1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile("python")


# Problem 2
def prob2():
    """Compile and return a regular expression pattern object that matches
    the string "^{@}(?)[%]{.}(*)[_]{&}$".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"\^\{\@\}\(\?\)\[\%\]\{\.\}\(\*\)\[\_\]\{\&\}\$")

# Problem 3
def prob3():
    """Compile and return a regular expression pattern object that matches
    the following strings (and no other strings).

        Book store          Mattress store          Grocery store
        Book supplier       Mattress supplier       Grocery supplier

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    pattern = re.compile(r"^(Book|Grocery|Mattress) (store|supplier)$")
    return pattern

# Problem 4
def prob4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    pattern = re.compile(r"^(^[a-zA-Z]|_)(\w|_)*$")
    """lst = ["3rats", "err*r", "sq(x)", "sleep()", " x", "Mouse", "compile", "_123456789", "__x__", "while"]
    for string in lst:
        print(string, bool(pattern.match(string)))"""
    return pattern

# Problem 5
def prob5(code):
    """Use regular expressions to place colons in the appropriate spots of the
    input string, representing Python code. You may assume that every possible
    colon is missing in the input string.

    Parameters:
        code (str): a string of Python code without any colons.

    Returns:
        (str): code, but with the colons inserted in the right places.
    """
    pattern = re.compile(r"(\s*if.*)|(elif.*)|(else)|(\s*for.*)|(while.*)|(try)|(except.*)|(except)|(finally)|(with.*)|(def.*)|(class.*)", re.MULTILINE)
    return pattern.sub(r"\1\2\3\4\5\6\7\8\9\10\11\12:", code)

# Problem 6
def prob6(filename="fake_contacts.txt"):
    """Use regular expressions to parse the data in the given file and format
    it uniformly, writing birthdays as mm/dd/yyyy and phone numbers as
    (xxx)xxx-xxxx. Construct a dictionary where the key is the name of an
    individual and the value is another dictionary containing their
    information. Each of these inner dictionaries should have the keys
    "birthday", "email", and "phone". In the case of missing data, map the key
    to None.

    Returns:
        (dict): a dictionary mapping names to a dictionary of personal info.
    """
    # Create dictionary and read data
    people = dict()
    f = open(filename)
    data = f.readlines()
    # Create the regular expressions to parse the data
    names = re.compile(r"^\w* \w\. \w*|^\w* \w\w\w*")
    email = re.compile(r"\S*@\S*")
    correctDate = re.compile(r"\d\d/\d\d/\d\d\d\d")
    birthday = re.compile(r"(\d*)/(\d*)/(\d*)")
    phone = re.compile(r"\((\d{3,3})\)(\d{3,3}-\d{4,4})|(\d{3,3})-(\d{3,3}-\d{4,4})|\d-(\d{3,3})-(\d{3,3}-\d{4,4})|\((\d{3,3})\)-(\d{3,3}-\d{4,4})")
    correctPhone = re.compile(r"\(\d*\)\d*-\d*")

    for line in data: # For every person, initialize their info as NULL and check for what information is applicable
        
        personBirthday = None
        personEmail = None
        personPhone = None
        if bool(birthday.search(line)):
            birthdays = birthday.findall(line) # gives a list of a tuple of the form (month, day, year)
            
            mlen = len(birthdays[0][0])
            dlen = len(birthdays[0][1])
            ylen = len(birthdays[0][2])
            # Depending on the format of the date, reformat the date to the correct form.
            if mlen == 1 and dlen == 1 and ylen == 2:
                corrected = birthday.sub(r"0\1/0\2/20\3", line)
            if mlen == 1 and dlen == 2 and ylen == 2:
                corrected = birthday.sub(r"0\1/\2/20\3", line)
            if mlen == 1 and dlen == 1 and ylen == 4:
                corrected = birthday.sub(r"0\1/0\2/\3", line)
            if mlen == 1 and dlen == 2 and ylen == 4:
                corrected = birthday.sub(r"0\1/\2/\3", line)
            if mlen == 2 and dlen == 1 and ylen == 2:
                corrected = birthday.sub(r"\1/0\2/20\3", line)
            if mlen == 2 and dlen == 2 and ylen == 2:
                corrected = birthday.sub(r"\1/\2/20\3", line)
            if mlen == 2 and dlen == 1 and ylen == 4:
                corrected = birthday.sub(r"\1/0\2/\3", line)
            if mlen == 2 and dlen == 2 and ylen == 4:
                corrected = birthday.sub(r"\1/\2/\3", line)
            personBirthday = correctDate.findall(corrected)[0]
            
        if bool(email.search(line)):
            personEmail = email.findall(line)[0]

        if bool(phone.search(line)):
            personPhone = phone.findall(line)[0]
            personPhone = phone.sub(r"(\1\3\5\7)\2\4\6\8", line)
            personPhone = correctPhone.findall(personPhone)[0]
            

        # Put each person in a dictionary mapping to their information.
        people[names.findall(line)[0]] = {"birthday": personBirthday, 
                                          "email": personEmail,
                                          "phone": personPhone}
                                          
    return people




    
    
    
