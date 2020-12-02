# test_specs.py
"""Python Essentials: Unit Testing.
<Name>
<Class>
<Date>
"""

import specs
import pytest


def test_add():
    assert specs.add(1, 3) == 4, "failed on positive integers"
    assert specs.add(-5, -7) == -12, "failed on negative integers"
    assert specs.add(-6, 14) == 8

def test_divide():
    assert specs.divide(4,2) == 2, "integer division"
    assert specs.divide(5,4) == 1.25, "float division"
    with pytest.raises(ZeroDivisionError) as excinfo:
        specs.divide(4, 0)
    assert excinfo.value.args[0] == "second input cannot be zero"


# Problem 1: write a unit test for specs.smallest_factor(), then correct it.
def test_factor():
    assert specs.smallest_factor(20) == 2, "Failed for composite numbers"
    assert specs.smallest_factor(171) == 3, "failed for prime numbers"
    assert specs.smallest_factor(2) == 2, "ok"
    assert specs.smallest_factor(9) == 3, "failed for square numbers"
    assert specs.smallest_factor(1857437) == 17, "woah dude"

# Problem 2: write a unit test for specs.month_length().
def test_prob2():
    assert specs.month_length('February', True) == 29, "Leap year incorrect"
    assert specs.month_length('September', True) == 30, "short month incorrect"
    assert specs.month_length('February', False) == 28, "Non leap year incorrect"
    assert specs.month_length('January', True) == 31, "long month incorrect"
    assert specs.month_length('Octobuary', True) == None, "incorrect name not implemented."

# Problem 3: write a unit test for specs.operate().
def test_operate():
    with pytest.raises(TypeError) as excinfo:
        specs.operate(1, 2, 3)
    assert excinfo.value.args[0] == "oper must be a string"
    assert specs.operate(1, 2, '+') == 3, "Failed for addition"
    assert specs.operate(2, 1, '-') == 1, "Failed for subtraction"
    assert specs.operate(3, 4, '*') == 12, "Failed for multiplication"
    with pytest.raises(ZeroDivisionError) as excinfo:
        specs.operate(1, 0, '/')
    assert excinfo.value.args[0] == "division by zero is undefined"
    assert specs.operate(12, 6, '/') == 2, "integer division"
    assert specs.operate(11, 5, '/') == 2.2, "float division"
    with pytest.raises(ValueError) as excinfo:
        specs.operate(1, 0, 'hi there')
    assert excinfo.value.args[0] == "oper must be one of '+', '/', '-', or '*'"

# Problem 4: write unit tests for specs.Fraction, then correct it.
@pytest.fixture
def set_up_fractions():
    frac_1_3 = specs.Fraction(1, 3)
    frac_1_2 = specs.Fraction(1, 2)
    frac_n2_3 = specs.Fraction(-2, 3)
    return frac_1_3, frac_1_2, frac_n2_3

def test_fraction_init(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_3.numer == 1
    assert frac_1_2.denom == 2
    assert frac_n2_3.numer == -2
    frac = specs.Fraction(30, 42)
    assert frac.numer == 5
    assert frac.denom == 7
    with pytest.raises(ZeroDivisionError) as excinfo:
        specs.Fraction(3, 0)
    assert excinfo.value.args[0] == "denominator cannot be zero"
    with pytest.raises(TypeError) as excinfo:
        specs.Fraction(2.4, 2.5)
    assert excinfo.value.args[0] == "numerator and denominator must be integers"

def test_fraction_str(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert str(frac_1_3) == "1/3"
    assert str(frac_1_2) == "1/2"
    assert str(frac_n2_3) == "-2/3"
    assert str(specs.Fraction(3, 1)) == "3"

def test_fraction_float(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert float(frac_1_3) == 1 / 3.
    assert float(frac_1_2) == .5
    assert float(frac_n2_3) == -2 / 3.

def test_fraction_eq(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert frac_1_2 == specs.Fraction(1, 2)
    assert frac_1_3 == specs.Fraction(2, 6)
    assert frac_n2_3 == specs.Fraction(8, -12)
    assert frac_1_2 == 0.5

def test_fraction_add(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert str(frac_1_3 + frac_1_2) == str(specs.Fraction(5, 6))

def test_fraction_sub(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert str(frac_1_2 - frac_1_3) == str(specs.Fraction(1, 6))

def test_fraction_mult(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    assert str(frac_1_2 * frac_1_3) == str(specs.Fraction(1, 6))

def test_fraction_truediv(set_up_fractions):
    frac_1_3, frac_1_2, frac_n2_3 = set_up_fractions
    with pytest.raises(ZeroDivisionError) as excinfo:
        frac_1_3 / specs.Fraction(0, 3)
    assert excinfo.value.args[0] == "cannot divide by zero"
    assert str(frac_1_3 / frac_1_2) == str(specs.Fraction(2, 3))


# Problem 5: Write test cases for Set.
def test_count_sets():
    hand1 = ["1022", "1122", "0100", "2021",
             "0010", "2201", "2111", "0020",
             "1102", "0210", "2110", "1020"]
    assert specs.count_sets(hand1) == 6
    hand2 = ["1022", "1122", "0100", "2021",
             "0010", "2201", "2111", "0020",
             "1102", "0210", "2110", "1020", "1112"]
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(hand2)
    assert excinfo.value.args[0] == "need list of 12 elements"
    hand3 = ["1122", "1122", "0100", "2021",
             "0010", "2201", "2111", "0020",
             "1102", "0210", "2110", "1020"]
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(hand3)
    assert excinfo.value.args[0] == "not all cards are unique"
    hand4 = ["122", "1122", "0100", "2021",
             "0010", "2201", "2111", "0020",
             "1102", "0210", "2110", "1020"]
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(hand4)
    assert excinfo.value.args[0] == "one or more cards not 4 digits"
    hand5 = ["1062", "1122", "0100", "2021",
             "0010", "2201", "2111", "0020",
             "1102", "0210", "2110", "1020"]
    with pytest.raises(ValueError) as excinfo:
        specs.count_sets(hand5)
    assert excinfo.value.args[0] == "one or more cards contains digit not 0, 1 ,2"

def test_is_set():
    assert specs.is_set("1022", "1122", "1020") == False
    assert specs.is_set("1111", "2012", "0210") == True
