# DataScienceEssentials

My solutions to the data science labs from BYU's Applied and Computational Mathematics Emphasis (ACME): SQL, regular expressions, web scraping, pandas, and tools for large or distributed data. Each lab is a notebook that pairs the problem statements with my solutions and their output, plus condensed notes on the concepts the lab covers.

| Lab | Source | Notebook |
|-----|--------|----------|
| SQL 1: Introduction | DSE, Lab 1 | [SQL1/sql1.ipynb](SQL1/sql1.ipynb) |
| SQL 2 (The Sequel) | DSE, Lab 2 | [SQL2/sql2.ipynb](SQL2/sql2.ipynb) |
| Regular Expressions | DSE, Lab 3 | [RegularExpressions/regular_expressions.ipynb](RegularExpressions/regular_expressions.ipynb) |
| Web Technologies | DSE, Lab 4 | [WebTechnologies/web_technologies.ipynb](WebTechnologies/web_technologies.ipynb) |
| Introduction to Beautiful Soup | DSE, Lab 5 | [WebScraping1/web_scraping1.ipynb](WebScraping1/web_scraping1.ipynb) |
| Advanced Web Scraping Techniques | DSE, Lab 6 | Not completed |
| Web Crawling | DSE (Jan 2019 ed.), Lab 6 | [WebCrawling/web_crawling.ipynb](WebCrawling/web_crawling.ipynb)* |
| Pandas 1: Introduction | DSE, Lab 7 | [Pandas1/pandas1.ipynb](Pandas1/pandas1.ipynb) |
| Pandas 2: Plotting | DSE, Lab 8 | [Pandas2/pandas2.ipynb](Pandas2/pandas2.ipynb) |
| Pandas 3: Grouping | DSE, Lab 9 | [Pandas3/pandas3.ipynb](Pandas3/pandas3.ipynb) |
| Pandas 4: Time Series | DSE, Lab 10 | [Pandas4/pandas4.ipynb](Pandas4/pandas4.ipynb) |
| Pandas 5 (GeoPandas) | Course lab | [Pandas5/pandas5.ipynb](Pandas5/pandas5.ipynb)* |
| MongoDB | Course lab | [MongoDB/mongodb.ipynb](MongoDB/mongodb.ipynb)* |
| iPyParallel: Intro to Parallel Programming | Course lab | [Parallel_Intro/parallel_intro.ipynb](Parallel_Intro/parallel_intro.ipynb)* |
| Spark | Course lab | [Spark/spark.ipynb](Spark/spark.ipynb)* |

Lab numbers follow the August 2018 edition of the *Data Science Essentials* (DSE) manual, which the course used in 2018–19. SQL 1 and SQL 2 are from 2017, when they were part of *Volume 2*. "Course lab" marks labs the course assigned from its own templates that weren't in the manual at the time. Problem statements are quoted from my lab templates where I had them, and from the manual otherwise. Each folder also keeps the grader feedback from my original submissions (`*_feedback.txt`).

\* Not re-run for this archive, since it needs a MongoDB server, PySpark, an ipyparallel cluster, GeoPandas, or 2018 versions of live websites. These notebooks show my original outputs where the lab was a notebook, and code only where it was a script.

## Running the notebooks

Each notebook runs from its own folder, with its data next to it. The notebooks need NumPy, pandas, Matplotlib, scikit-learn (for the iris data in Pandas 3), requests and Beautiful Soup. SQL 1 rebuilds `students.db` and `earthquakes.db` from the CSV files.

## Credits

The lab specifications come from the [Foundations of Applied Mathematics](https://foundations-of-applied-mathematics.github.io/) *Data Science Essentials* and *Volume 2* lab manuals, © Dr. J. Humpherys, licensed under [CC BY 3.0 US](http://creativecommons.org/licenses/by/3.0/us/). The data files come from the original lab materials. Problem statements are quoted from the specs and course templates; the solutions are my own.
