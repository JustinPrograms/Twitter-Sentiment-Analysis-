"""
All variables and function naming is done using snake case.
This file in particular is the sentiment analysis file where majority of the functions are executed.
"""


# Function to read keywords from a given file
def read_keywords(keyword_file_name):
    # Creating empty dictionary to store keywords from file and the value
    word_dict = {}

    try:
        # Open and read the file
        with open(keyword_file_name, "rt") as file:
            # Process each line in the file
            for line in file:
                # Split line into keyword and value, then add to dictionary
                line_split = line.strip().split("\t")
                word_dict[line_split[0]] = line_split[1]
        file.close()
    except IOError:
        # Handle file open error
        print(f"Could not open file {keyword_file_name}!")

    # Return the dictionary
    return word_dict


# Function to remove non-alphabetic letters and to convert to lowercase from given tweet text
def clean_tweet_text(tweet_text):
    # Convert text to lowercase
    tweet_text = tweet_text.lower()

    # Remove non-alphabetic characters (except spaces)
    for char in tweet_text:
        if not (97 <= ord(char) <= 122) and ord(char) != 32:
            tweet_text = tweet_text.replace(char, "")

    # Return the cleaned tweet text
    return tweet_text


# Function to calculate the sentiment score from taking the clean tweet text and comparing words to the keyword dictonary
def calc_sentiment(tweet_text, keyword_dict):
    # Initialize sentiment score
    sentiment_score = 0

    # Split tweet text into words
    words = tweet_text.split()

    # Calculate sentiment score based on keywords
    for word in words:
        if word in keyword_dict:
            sentiment_score += int(keyword_dict[word])

    # Return the calculated sentiment score
    return sentiment_score


# Function to classify the sentiment score from given score that was calculated
def classify(score):
    # Classify sentiment based on the score
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"


# Function to read the tweets from given tweets file and organize the information
def read_tweets(tweet_file_name):
    # List to store dictionaries representing tweets
    tweets_list = []

    try:
        # Open and read the specified file
        with open(tweet_file_name, "rt") as file:
            # Process each line in the file
            for line in file:
                # Split line into values
                line_split = line.strip().split(",")

                # Convert integer to float if not NULL
                if line_split[9] != "NULL":
                    line_split[9] = float(line_split[9])

                if line_split[10] != "NULL":
                    line_split[10] = float(line_split[10])

                # Create a dictionary representing a tweet and add to the list
                tweets_dic = {"date": line_split[0],
                              "text": clean_tweet_text(line_split[1]),
                              "user": line_split[2],
                              "retweet": int(line_split[3]),
                              "favorite": int(line_split[4]),
                              "lang": line_split[5],
                              "country": line_split[6],
                              "state": line_split[7],
                              "city": line_split[8],
                              "lat": line_split[9],
                              "lon": line_split[10]}
                tweets_list.append(tweets_dic)
        file.close()
    except IOError:
        # Handle file open error
        print(f"Could not open file {tweet_file_name}")

    # Return the list of tweets
    return tweets_list


# Function to make a report using all information from the tweet_list and the keyword dictionary
def make_report(tweet_list, keyword_dict):
    # Initialize variables
    num_of_tweets = 0
    total_sentiment_score = 0
    positive_tweets = 0
    negative_tweets = 0
    neutral_tweets = 0
    total_favorite = 0
    num_of_favorite = 0
    num_retweets = 0
    score_retweets = 0
    country_scores = {}

    # Process each tweet in the list
    for tweet in tweet_list:
        clean_tweet = clean_tweet_text(tweet["text"])
        sentiment_score = calc_sentiment(clean_tweet, keyword_dict)

        country = tweet["country"]

        # Update country scores
        if country not in country_scores:
            country_scores[country] = {
                "score": sentiment_score,
                "count": 1
            }
        else:
            country_scores[country]["score"] += sentiment_score
            country_scores[country]["count"] += 1

        # Update sentiment counts
        if classify(sentiment_score) == "positive":
            positive_tweets += 1
        elif classify(sentiment_score) == "negative":
            negative_tweets += 1
        else:
            neutral_tweets += 1
        total_sentiment_score += sentiment_score

        # Update retweet information
        if int(tweet["retweet"]) > 0:
            num_retweets += 1
            score_retweets += sentiment_score

        # Update favorite information
        if int(tweet["favorite"]) > 0:
            total_favorite += sentiment_score
            num_of_favorite += 1

        num_of_tweets += 1

    # Calculate averages and round to two decimal places
    avg_sentiment_score = round(total_sentiment_score / num_of_tweets, 2)
    avg_favorite = round(total_favorite / num_of_favorite, 2)
    avg_sentiment_score_retweets = round(score_retweets / num_retweets, 2)

    # Calculate country average scores and sort by average score
    for country, data in country_scores.items():
        country_scores[country]["avg_score"] = round(data["score"] / data["count"], 2)

    sorted_countries = sorted(country_scores.items(), key=lambda x: (x[1]["avg_score"],), reverse=True)

    # Exclude "NULL" if present
    if "NULL" in [country for country, data in sorted_countries]:
        sorted_countries = [(country, data) for country, data in sorted_countries if country != "NULL"]

    # Get top five countries
    top_countries = [country for country, data in sorted_countries[:5]]
    top_countries_string = ", ".join(top_countries)

    # Create report dictionary
    report_dict = {
        "avg_favorite": avg_favorite,
        "avg_retweet": avg_sentiment_score_retweets,
        "avg_sentiment": avg_sentiment_score,
        "num_favorite": num_of_favorite,
        "num_negative": negative_tweets,
        "num_neutral": neutral_tweets,
        "num_positive": positive_tweets,
        "num_retweet": num_retweets,
        "num_tweets": num_of_tweets,
        "top_five": top_countries_string
    }

    return report_dict


# Function to export the report that was made to a output file and format it
def write_report(report, output_file):
    # Write report to the specified output file
    with open(output_file, 'w') as file:
        file.write("Average sentiment of all tweets: " + str(report["avg_sentiment"]) + "\n")
        file.write("Total number of tweets: " + str(report["num_tweets"]) + "\n")
        file.write("Number of positive tweets: " + str(report["num_positive"]) + "\n")
        file.write("Number of negative tweets: " + str(report["num_negative"]) + "\n")
        file.write("Number of neutral tweets: " + str(report["num_neutral"]) + "\n")
        file.write("Number of favorited tweets: " + str(report["num_favorite"]) + "\n")
        file.write("Average sentiment of favorited tweets: " + str(report["avg_favorite"]) + "\n")
        file.write("Number of retweeted tweets: " + str(report["num_retweet"]) + "\n")
        file.write("Average sentiment of retweeted tweets: " + str(report["avg_retweet"]) + "\n")
        file.write("Top five countries by average sentiment: " + str(report["top_five"]) + "\n")
    file.close()

    print(f"Wrote report to {output_file}")
