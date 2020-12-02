# python_intro.py
"""Python Essentials: Introduction to Python.
<Name> William Terry
<Class> Math 321 Section 004
<Date> 9/2/20
"""
def sphere_volume(r):
    """Return the volume of a sphere with radius r"""
    v = (4 / 3) * 3.14159 * (r ** 3)
    return v

def isolate(a, b, c, d, e):
    print(a, b, c, sep="     ", end=" ")
    print(d, e, sep=" ")

def first_half(str):
    x = len(str)
    str = (str[:(x // 2)])
    return str

def backward(str):
    str = str[-1::-1]
    return str

def list_ops():
    list = ["bear", "ant", "cat", "dog"]
    list.append("eagle")
    list[2] = "fox"
    list.remove(list[1])
    list.sort(reverse=True)
    list[list.index("eagle")] = "hawk"
    list[-1] = list[-1] + "hunter"
    return list

def pig_latin(word):
    if word[0] in ['a', 'e', 'i'' o', 'u', 'A', 'E', 'I', 'O', 'U']:
        word = word + "hay"

    else:
        x = word[0]
        word = word[1:] + x + "ay"

    return word

def palindrome():
    x = 0
    for i in range(100, 999):
        for j in range(100, 999):
            w = i * j
            if w > x:
                s = str(i * j)
                if s == s[::-1]:
                    x = i * j

    return x


def alt_harmonic(n):
    list_output = [((-1) ** (i + 1)) / int(i) for i in range(1, n + 1)]

    return sum(list_output)


if __name__ == "__main__":
    print("Hello world!")
    print(sphere_volume(3))
    isolate(1, 2, 3, 4, 5)
    print(first_half("test"))
    print(backward("test"))
    print(list_ops())
    print(pig_latin("Aloe"))
    print(palindrome())
    print(alt_harmonic(500000))




