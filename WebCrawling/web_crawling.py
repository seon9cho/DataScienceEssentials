"""Volume 3: Web Scraping 2.
<Name>
<Class>
<Date>
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import matplotlib.pyplot as plt

# Problem 1
def scrape_books(start_page = "index.html"):
    """ Crawl through http://books.toscrape.com and extract fiction data"""
    
    # Initialize variables, including a regex for finding the 'next' link.
    base_url="http://books.toscrape.com/catalogue/category/books/fiction_10/"
    price_total = []
    count_total = []
    page = base_url + start_page                # Complete page URL.
    next_page_finder = re.compile(r"next")      # We need this button.
    current = None

    for _ in range(4):
        total = 0
        count = 0
        
        while current == None:                   # Try downloading until it works.
            # Download the page source and PAUSE before continuing.  
            page_source = requests.get(page).text
            time.sleep(1)           # PAUSE before continuing.
            soup = BeautifulSoup(page_source, "html.parser")
            current = soup.find_all(class_="price_color")
            
        #Extract the price data.
        for price in current:
            total += float(price.string.strip("Â£"))
            count += 1

        price_total.append(total)
        count_total.append(count)
    

        if "page-4" not in page:
            # Find the URL for the page with the next data.
            new_page = soup.find(string=next_page_finder).parent["href"]    
            page = base_url + new_page      # New complete page URL.
            current = None
        else:
            # Calculate the price average
            average_price = sum(price_total)/sum(count_total)

    return average_price

# Problem 2
def bank_data():
    """Crawl through the Federal Reserve site and extract bank data."""
    # Compile regular expressions for finding certain tags.
    link_finder = re.compile(r"^December 31, 20(1[0-8]|0[4-9])")
    chase_bank_finder = re.compile(r"^JPMORGAN CHASE BK")
    bank_of_america_finder = re.compile(r"^BANK OF AMER")
    wells_fargo_finder = re.compile(r"^WELLS FARGO BK")

    # Get the base page and find the URLs to all other relevant pages.
    base_url="https://www.federalreserve.gov/releases/lbr/"
    base_page_source = requests.get(base_url).text
    base_soup = BeautifulSoup(base_page_source, "html.parser")
    link_tags = base_soup.find_all(name='a', href=True, string=link_finder)
    pages = [base_url + tag.attrs["href"] for tag in link_tags]

    # Crawl through the individual pages and record the data.
    chase_assets = []
    boa_assets = []
    wf_assets = []
    for page in pages:
        time.sleep(1)               # PAUSE, then request the page.
        soup = BeautifulSoup(requests.get(page).text, "html.parser")
        print(page)
        # Find the tag corresponding to Chase Banks's consolidated assets.
        chase_temp_tag = soup.find(name="td", string=chase_bank_finder)
        boa_temp_tag = soup.find(name="td", string=bank_of_america_finder)
        wf_temp_tag = soup.find(name="td", string=wells_fargo_finder)
        for _ in range(10):
            chase_temp_tag = chase_temp_tag.next_sibling
            boa_temp_tag = boa_temp_tag.next_sibling
            wf_temp_tag = wf_temp_tag.next_sibling

        # Extract the data, removing commas.
        chase_assets.append(int(chase_temp_tag.string.replace(',', '')))
        boa_assets.append(int(boa_temp_tag.string.replace(',', '')))
        wf_assets.append(int(wf_temp_tag.string.replace(',', '')))

    # data to plot
    n_groups = 14
    means_frank = (90, 55, 40, 65)
    means_guido = (85, 62, 54, 20)
     
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2
     
    rects1 = plt.bar(index, chase_assets, bar_width,
                     label='Chase Bank')
    rects2 = plt.bar(index + bar_width, boa_assets, bar_width,
                     label='Bank of America')
    rects2 = plt.bar(index + 2*bar_width, wf_assets, bar_width,
                     label='Wells Fargo')

    plt.xlabel('Year')
    plt.ylabel('Mil $')
    plt.title('Consolidated assets of each bank')
    plt.xticks(index + bar_width, [year for year in range(2017, 2003, -1)])
    plt.legend()
     
    plt.tight_layout()
    plt.show()


# Problem 3
def prob3():
    """The Basketball Reference website at https://www.basketball-reference.com
    contains data on NBA athletes, including which player led different categories 
    for each season. For the past ten seasons, identify which player had the most 
    season points and find how many points they scored during that season. Return 
    a list of triples consisting of the season, the player, and the points scored, 
    ("season year", "player name", points scored).
    """
    # Base url
    base_url = "https://www.basketball-reference.com"
    base_source = requests.get(base_url + "/leagues").text
    base_soup = BeautifulSoup(base_source, "html.parser")
    # Seasons we're interested in
    seasons = [str(year) for year in range(2018, 2008, -1)]
    most_points = []
    for season in seasons:
        year = season[-2:]
        season_str = str(int(season) - 1) + "-" + year
        row = base_soup.find_all(name='a', href=True, string=season_str)[1]
        season_tag = row.parent
        # Search to the right tag
        for i in range(5):
            season_tag = season_tag.next_sibling
        # Get the name and year
        name = ' '.join(season_tag.text.split()[:2])
        year = season_tag.text.split()[2].replace("(", "").replace(")", "")
        # Add to list
        most_points.append((season, name, int(year)))

    return most_points

# Problem 4
def prob4(search_query):
    """Use Selenium to enter the given search query into the search bar of
    https://arxiv.org and press Enter. The resulting page has up to 25 links
    to the PDFs of technical papers that match the query. Gather these URLs,
    then continue to the next page (if there are more results) and continue
    gathering links until obtaining at most 100 URLs. Return the list of URLs.

    Returns:
        (list): Up to 100 URLs that lead directly to PDFs on arXiv.
    """
    # Open browser through Selenium
    browser = webdriver.Chrome()
    urls = []
    try:
        # Open the webpage
        browser.get("https://arxiv.org")
        try:
            # Search the query
            search_bar = browser.find_element_by_name('query')
            search_bar.clear()
            search_bar.send_keys(search_query)
            search_bar.send_keys(Keys.RETURN)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            # Find the urls of the pdfs
            url = soup.find_all(name='a', href=True, string='pdf')
            urls += url
            # Search through the next pages if it exists until we get 150 total
            try:
                while len(urls) < 150:
                    browser.find_element_by_class_name("pagination-next").send_keys(Keys.RETURN)
                    soup = BeautifulSoup(browser.page_source, "html.parser")
                    url = soup.find_all(name='a', href=True, string='pdf')
                    urls += url
            except NoSuchElementException:
                pass

        except NoSuchElementException:
            print("Could not find the search bar!")
            raise
    finally:
        # Close browser
        browser.close()

    return urls


# Problem 5
def prob5():
    """For each of the (at least) 600 problems in the archive at
    https://projecteuler.net/archives, record the problem ID and the number of
    people who have solved it. Return a list of IDs, sorted from largest to
    smallest by the number of people who have solved them. That is, the first
    entry in the list should be the ID of the most solved problem, and the
    last entry in the list should be the ID of the least solved problem.

    Returns:
        (list): problem IDs (as strings), from most solved to least solved.
    """    
    # Open broswer through Selenium
    browser = webdriver.Chrome()
    problems = []
    try:
        # Go to the webpage
        browser.get("https://projecteuler.net/archives")
        page = 1
        # Go through each of the pages
        while True:
            soup = BeautifulSoup(browser.page_source, "html.parser")
            # Regex for href
            re_href = re.compile(r"^problem=\d+$")
            # Find all the problems
            prob = soup.find_all(name='a', href=re_href)
            # Navigate to the tags with the id and num solved and add to list
            for p in prob:
                id_num = list(list(p.parents)[1].children)[0].text
                num_solved = list(list(p.parents)[1].children)[2].text
                problems.append([int(id_num), int(num_solved)])
            try:
                # Do this for all the other pages
                page += 1
                pg_str = "Go to page " + str(page)
                browser.find_element_by_xpath('//*[@title="{}"]'.format(pg_str)).send_keys(Keys.RETURN)
            except NoSuchElementException:
                print("{} doesn't exist".format(pg_str))
                break

    finally:
        # Close browser
        browser.close()

    problems.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in problems]

