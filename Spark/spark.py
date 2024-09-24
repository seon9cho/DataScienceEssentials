# solutions.py
"""Volume 3: Spark.
<Name>
<Class>
<Date>
"""


import pyspark
from pyspark.sql import SparkSession
import numpy as np

# Problem 1
def prob1(filename='mathematicians.csv'):
    """Reads in a csv file of mathematicians and reduces it to the names
    of the female mathemticians born in the 19th century. Returns a list
    of the first 5 of these names.
    """
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.option("header", True).csv(filename)
    out = df.filter(df.gender=="female").filter(df.birth_year.between(1801, 1900))
    names = out.select("name").rdd.flatMap(lambda x: x).collect()[:5]
    spark.stop()
    return names

# Problem 2
def prob2(filename='mathematicians.csv'):
    """Reads in a csv file of mathematicians, groups the
    data by country of citizenship, counts the number of occurrences of each country,
    and returns a list of the top 5 countries and their counts.
    """
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.option("header", True).csv(filename)
    out = df.groupBy("country").count().orderBy("count", ascending=False)
    count_count = out.rdd.map(lambda x: x[:2]).collect()[:5]
    spark.stop()
    return count_count

# Problem 3
def sortCount(filename='yoda.txt'):
    """Simple sorted word count function.

    Parameters:
        file (str): text file

    Returns:
        output[:5] (list): the first five (word, count) pairs
    """
    spark = SparkSession.builder.getOrCreate()
    RDD = spark.read.text(filename)\
                .rdd\
                .map(lambda x: x[0])\
                .flatMap(lambda x: x.split(" "))\
                .map(lambda x: (x,))
    df = RDD.toDF().groupBy("_1").count().orderBy("count", ascending=False)
    word_count = df.rdd.map(lambda x: x[:2]).collect()[:5]
    spark.stop()
    return word_count

# Problem 4
def pi(partitions=2):
    """Simple Monte-Carlo routine to estimate the area of the
    unit circle (i.e. the value of pi).

    Parameters:
        partitions (int): number of partitions to run the calculation with
            (number of partitions specifies the number of nodes to use)

    Returns an estimated value of pi.
    """
    try:
        p = 1e5
        sc = pyspark.context.SparkContext()
        l = sc.parallelize(range(int(p*partitions)), partitions)\
                    .map(lambda x: np.random.uniform(-1, 1, 2))\
                    .map(lambda x: np.linalg.norm(x) <= 1)\
                    .reduce(lambda a, b: int(a) + int(b))
        return l/(2*p)*4
    finally:
        sc.stop()
