"""Volume 3: Introduction to BeautifulSoup.
<Name>
<Class>
<Date>
"""

import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
# Example HTML string from the lab.
pig_html = """
<html><head><title>Three Little Pigs</title></head>
<body>
<p class="title"><b>The Three Little Pigs</b></p>
<p class="story">Once upon a time, there were three little pigs named
<a href="http://example.com/larry" class="pig" id="link1">Larry,</a>
<a href="http://example.com/mo" class="pig" id="link2">Mo</a>, and
<a href="http://example.com/curly" class="pig" id="link3">Curly.</a>
<p>The three pigs had an odd fascination with experimental construction.</p>
<p>...</p>
</body></html>
"""

def prob1():
    """
    Use the requests library to get the HTML source for the website http://www.example.com.
    Save the source as a file called 'example.html'. If the file already exists, make
    sure not to scrape the website, or overwrite the file.
    """
    import os.path
    # Check if file exists
    if not os.path.isfile("example.html"):
        # Write example.html
        response = requests.get("http://www.example.com")
        with open("example.html", 'w') as outfile:
            outfile.write(response.text)
            print("File written")
    else:
        raise "example.html already exists"


# Problem 1
def prob2():
    """Examine the source code of http://www.example.com. Determine the names
    of the tags in the code and the value of the 'type' attribute associated
    with the 'style' tag.

    Returns:
        (set): A set of strings, each of which is the name of a tag.
        (str): The value of the 'type' attribute in the 'style' tag.
    """
    tags = set()
    style_type = None
    # Open example.html, then read each line
    with open("example.html", 'r') as infile:
        for line in infile.readlines():
            # Search for tags
            if re.search(r'</?(\w+) ?.*>', line):
                tags = tags.union(set(re.findall(r'</?(\w+) ?[^>]*>', line)))
            # Search for the value of the 'type' attribute
            if re.search(r'<style type=\"[^>\"]+\">', line):
                style_type = re.search(r'<style type=\"([^>\"]+)\">', line).group(1)
    return tags, style_type

# Problem 2
def prob3(code):
    """Return a list of the names of the tags in the given HTML code."""
    # Parse code with bs4
    soup = BeautifulSoup(code, 'html.parser')
    # Return the tag name of each tag
    return [s.name for s in soup.find_all(True)]


# Problem 3
def prob4(filename="example.html"):
    """Read the specified file and load it into BeautifulSoup. Find the only
    <a> tag with a hyperlink and return its text.
    """
    # Parse file with bs4
    with open(filename, 'r') as infile:
        soup = BeautifulSoup(infile.read(), 'html.parser')
    # Find the <a> tag with a hyperlink
    a_tag = soup.a
    return a_tag.text


# Problem 4
def prob5(filename="san_diego_weather.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the following tags:

    1. The tag containing the date 'Thursday, January 1, 2015'.
    2. The tags which contain the links 'Previous Day' and 'Next Day'.
    3. The tag which contains the number associated with the Actual Max
        Temperature.

    Returns:
        (list) A list of bs4.element.Tag objects (NOT text).
    """
    # Parse file with bs4
    with open(filename, 'r') as infile:
        soup = BeautifulSoup(infile.read(), 'html.parser')
    # Search for the date
    date_tag = soup.find(string="Thursday, January 1, 2015").parent
    # Search for Previous Day and Next Day
    PND_tags = [s.parent for s in soup.findAll(string=re.compile("Previous Day")) if "href" in s.parent.attrs]
    PND_tags += [s.parent for s in soup.findAll(string=re.compile("Next Day")) if "href" in s.parent.attrs]
    # Traverse through Max Temperature to find Actual Max Temperature
    AMT_tag = soup.find(string="Max Temperature").parent.parent.next_sibling.next_sibling.children
    next(AMT_tag)
    AMT_tag = next(AMT_tag).children
    AMT_tag = next(AMT_tag)

    return [date_tag] + PND_tags + [AMT_tag] 

# Problem 5
def prob6(filename="large_banks_index.html"):
    """Read the specified file and load it into BeautifulSoup. Return a list
    of the tags containing the links to bank data from September 30, 2003 to
    December 31, 2014, where the dates are in reverse chronological order.

    Returns:
        (list): A list of bs4.element.Tag objects (NOT text).
    """
    # Parse file with bs4
    with open(filename, 'r') as infile:
        soup = BeautifulSoup(infile.read(), 'html.parser')
    # Use Regex to find all the dates between September 30, 2003 to December 31, 2014
    date_regex = re.compile(r"((March|June|September|December) 3[01], (200[4-9]|201[0-4])|(September|December) 3[01], 2003)")
    # Get the tags of all occurrences
    tags = [s.parent for s in soup.findAll(string=date_regex)]
    return tags

# Problem 6
def prob7(filename="large_banks_data.html"):
    """Read the specified file and load it into BeautifulSoup. Create a single
    figure with two subplots:

    1. A sorted bar chart of the seven banks with the most domestic branches.
    2. A sorted bar chart of the seven banks with the most foreign branches.

    In the case of a tie, sort the banks alphabetically by name.
    """
    # Parse file with bs4
    with open(filename, 'r') as infile:
        soup = BeautifulSoup(infile.read(), 'html.parser')
    # Find the table
    table = soup.findAll(name="tr", valign="TOP")
    # Save the name, # domestic branches, and # foreign branches as a tuple
    bank_info = [(list(t.children)[1].text.split('/')[0], 
                int(list(t.children)[19].text.replace(',', '')), 
                int(list(t.children)[21].text.replace(',', ''))) 
                for t in table[1:]
                if list(t.children)[19].text != "."]
    # Sort them separately first by the # of branches, then by name
    top_domestic = sorted(bank_info, key=lambda x: (x[1],x[0]))
    top_foreign = sorted(bank_info, key=lambda x: (x[2],x[0]))
    # Plot the first 7 top domestic branches
    ax = plt.subplot(211)
    plt.barh([t[0] for t in top_domestic[-7:]], 
               [t[1] for t in top_domestic[-7:]])
    plt.title("Top domestic")
    plt.yticks(fontsize=7, rotation=30)
    # Plot the first 7 top foreign branches
    plt.subplot(212)
    plt.barh([t[0] for t in top_foreign[-7:]],
               [t[2] for t in top_foreign[-7:]])
    plt.title("Top foreign")
    plt.yticks(fontsize=7, rotation=30)
    plt.tight_layout()
    plt.show()    

if __name__ == '__main__':
    with open("example.html", 'r') as infile:
        code = infile.read()
    print(prob2())
    print(prob3(code))
    print(prob4())
    print(prob5())
    prob6()
    prob7()

