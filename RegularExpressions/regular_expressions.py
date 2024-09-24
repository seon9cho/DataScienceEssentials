# regular_expressions.py
"""Volume 3: Regular Expressions.
Seong-Eun Cho
Volume3
9/10/18
"""
import re


# Problem 1
def prob1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"python")
        
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
    return re.compile(r"^(Book|Mattress|Grocery) (store|supplier)$")

# Problem 4
def prob4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"^[a-zA-Z_][\w_]* *(\= *(\d+\.?\d*|\'[^\']*\'|[a-zA-Z_][\w_]*))?$")

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
    # Define the patterns for each class of keywords
    pattern1 = re.compile(r"(if|elif|for|while|with|def|class)(.+)")
    pattern2 = re.compile(r"(else|try|finally)")
    pattern3 = re.compile(r"(except.*)")

    # Substitue in the colons
    code = pattern1.sub(r"\1\2:", code)
    code = pattern2.sub(r"\1:", code)
    code = pattern3.sub(r"\1:", code)

    return code

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
    # Open the file and save it as a list
    with open(filename, 'r') as infile:
        contacts = infile.readlines()
    
    # Determine the regexes for each field
    reg_name = re.compile(r'^\b[a-zA-Z]+\b ([A-Z]\. )?\b[a-zA-Z]+\b')
    reg_bday = re.compile(r'\d{1,2}\/\d{1,2}\/\d{2,4}')
    reg_email = re.compile(r'\S+@\w+(\.[a-zA-Z]+)+')
    reg_phone = re.compile(r'(\d\-)?\(?(\d{3,4})\)?\-?(\d{3,4})\-(\d{3,4})')

    contact_dict = dict()
    # Iterate through the contacts and save each entry into a dictionary
    for contact in contacts:
        d = dict()
        name = reg_name.search(contact).group(0)

        if reg_bday.search(contact):
            bday_list = reg_bday.search(contact).group(0).split('/')
            if len(bday_list[0]) == 1:
                bday_list[0] = "0" + bday_list[0]
            if len(bday_list[1]) == 1:
                bday_list[1] = "0" + bday_list[1]
            if len(bday_list[2]) == 2:
                bday_list[2] = "20" + bday_list[2]
            d["birthday"] = '/'.join(bday_list)
        else:
            d["birthday"] = None
        if reg_email.search(contact):
            d["email"] = reg_email.search(contact).group(0)
        else:
            d["email"] = None
        if reg_phone.search(contact):
            d["phone"] = reg_phone.sub(r"(\2)\3-\4", reg_phone.search(contact).group(0))
        else:
            d["phone"] = None

        contact_dict[name] = d

    return contact_dict


# Test function
def main():
    # Test prob1
    print("Testing prob1")
    print(prob1())

    # Test prob2
    print("\nTesting prob2")
    print(prob2())
    print("^{@}(?)[%]{.}(*)[_]{&}$")
    print("^{@}(?)[%]\{.\}(*)[_]{&}$")
    print(bool(re.match(prob2(), "^{@}(?)[%]{.}(*)[_]{&}$")))

    # Test prob3
    print("\nTesting prob3")
    print(bool(re.search(prob3(), "Book store")))
    print(bool(re.search(prob3(), "Mattress store")))
    print(bool(re.search(prob3(), "Grocery store")))
    print(bool(re.search(prob3(), "Book supplier")))
    print(bool(re.search(prob3(), "Mattress supplier")))
    print(bool(re.search(prob3(), "Grocery supplier")))

    # Test prob4
    print("\nTesting prob4")
    print("Matches:")
    print(bool(re.match(prob4(), "Mouse")))
    print(bool(re.match(prob4(), "compile")))
    print(bool(re.match(prob4(), "_123456789")))
    print(bool(re.match(prob4(), "__x__")))
    print(bool(re.match(prob4(), "while")))
    print("Non-matches:")
    print(bool(re.match(prob4(), "3rats")))
    print(bool(re.match(prob4(), "err*r")))
    print(bool(re.match(prob4(), "sq(x)")))
    print(bool(re.match(prob4(), "sleep()")))
    print(bool(re.match(prob4(), " x")))
    print("Matches:")
    print(bool(re.match(prob4(), "max=4.2")))
    print(bool(re.match(prob4(), "string= ''")))
    print(bool(re.match(prob4(), "num_guesses")))
    print("Non-matches:")
    print(bool(re.match(prob4(), "300")))
    print(bool(re.match(prob4(), "is_4=(value==4)")))
    print(bool(re.match(prob4(), "pattern = r'^one|two fish$'")))

    # Test prob5
    print("\nTesting prob5")
    code = (
        "k, i, p = 999, 1, 0\n"
        "while k > i\n"
        "\ti *= 2\n"
        "\tp += 1\n"
        "\tif k != 999\n"
        "\t\tprint(\"k should not have changed\") \n"
        "\telse\n"
        "\t\tpass\n"
        "print(p)")

    print(code)
    print(prob5(code))

    # Test prob6
    print("\nTesting prob6")
    contacts = prob6()
    print(contacts)

if __name__ == '__main__':
    main()
