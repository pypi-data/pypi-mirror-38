# Python wrapper for the webis Twitter sentiment evaluation ensemble

This is a Python wrapper around the Java implementation of a Twitter sentiment evaluation framework presented by [Hagen et al. (2015)](http://www.aclweb.org/anthology/S15-2097). The example script fetches Tweets from a PostgreSQL database, uses [PyJnius](https://github.com/kivy/pyjnius/tree/master/jnius) to call the Java modules to evaluate the sentiment, and saves results to a table in the same database.

### Dependencies

The script depends on the Python modules [PyJnius](https://github.com/kivy/pyjnius/tree/master/jnius), [pandas](https://pandas.pydata.org/) and [emojientities](https://gitlab.com/christoph.fink/python-emoji-range). 

On top of that, a Java Runtime Environment (jre) is required, plus a matching Java Development Kit (jdk). We used Java 8, but other versions might work just as well. [OpenJDK](https://openjdk.java.net/) works fine.

### Installation

- *using `pip` or similar:*

```shell
pip install webis
```

- *manually:*

    - Clone this repository

    ```shell
    git clone https://gitlab.com/christoph.fink/python-webis.git
    ```

    - Change to the cloned directory    
    - Use the Python `setuptools` to install the package:

    ```shell
    cd python-webis
    python ./setup.py install
    ```

### Usage

First, make sure the environment variable `JAVA_HOME` is set and pointing to your Java installation. 

Then instantiate a `webis.SentimentIdentifier` object and use its `identifySentiment()` function, passing in a list of tuples (`[(tweetId, tweetText),(tweetId, tweetText), … ]`) or a `pandas.DataFrame` (first column is treated as identifier, second as tweetText). 

The function returns a list of tuples (`[(tweetId, sentiment), … ]`) or a data frame (first column id, second column sentiment) of rows it successfully identified a sentiment of.

```python
import webis

sentimentIdentifier = webis.SentimentIdentifier()

tweets = [
    (1, "What a beautiful morning! There’s nothing better than cycling to work on a sunny day 🚲."),
    (2, "Argh, I hate it when you find seven (7!) cars blocking the bike lane on a five-mile commute")
]

sentimentIdentifier.identifySentiment(tweets)
# [(1, "positive"), (2, "negative")]

import pandas
tweets = pandas.DataFrame(tweets)
sentimentIdentifier.identifySentiment(tweets)
#   sentiment tweetId
# 0  positive       1
# 1  negative       2


```
