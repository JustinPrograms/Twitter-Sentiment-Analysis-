"""
All variables and function naming is done using snake case.
This program conducts sentiment analysis on February 2023 tweets to assess public opinion.
This file in particular is the main file where the program runs, receives user input and calls functions from another file.
"""
from sentiment_analysis import *


def main():
    # Get filenames for keywords, tweets, and output (.tsv, .csv, .txt), raise exception for wrong file extension
    keywords = input("Input keyword filename (.tsv file): ")
    if not keywords.endswith(".tsv"):
        raise Exception("Must have tsv file extension!")

    tweets = input("Input tweet filename (.csv file): ")
    if not tweets.endswith(".csv"):
        raise Exception("Must have csv file extension!")

    output = input("Input filename to output report in (.txt file): ")
    if not output.endswith(".txt"):
        raise Exception("Must have txt file extension!")

    # Reading the keywords and tweets from the provided files
    keyword_dict = read_keywords(keywords)
    read_tweet = read_tweets(tweets)

    # Checking if the keyword dictionary or tweet list is empty
    if not keyword_dict or not read_tweet:
        raise Exception("Tweet list or keyword dictionary is empty!")

    # Generating a sentiment analysis report and writing it to the specified output file
    write_report(make_report(read_tweet, keyword_dict), output)


# Calling the main function to start the sentiment analysis
main()
