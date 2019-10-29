
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import os
from textblob import TextBlob
import sys
import re


#user credentials Twitter API
consumer_key="ReElT98AQjypB3ci6jddzj6zi"
consumer_secret="P2miZKpbDhydB2lp8OlZvQUVHB2lW7cS9Px3bI9Xv0M4i8bist"
access_token="975795800134574080-MsFAepUwuaVBYc71skhORVEUimSTEOp"
access_token_secret="w2DPJhuJjvc0RwmYbKyFzK6Zmb2jkb29behisyawcrU5B"

#get authentication, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



#checking every minute the number of tweets on a twitter account
twitteraccount = "realdonaldtrump"
user = api.get_user(twitteraccount)
# print Twitter account name and the number of followers
print("screen_name: " + user.screen_name)
print("Number of followers: " + str(user.followers_count))
print("Following" + str(user.friends_count))
print("location: " + user.location)

file_object= open("tweets.json", "w")


def clean_tweet(tweet):  #only tweet text is allowed
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ /  \ /  \S+)", " ", tweet).split()) #removes links or special characters and emojis

def get_tweet_sentiment(tweet): #analysis of passed tweets
    # object of passed tweet text created
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        pibrella.light.green.on()
        return 'positive'

    elif analysis.sentiment.polarity == 0:
        pibrella.light.amber.on()
        return 'neutral'
    else:
        pibrella.light.red.on()
        return 'negative'

oldtime = time.time() #view of the actual time
while True:  #program obtains the latest four tweets
    if time.time() -oldtime > 59:
        oldtime = time.time()
        number_of_tweets = user.statuses_count
        # Retrieve the last four tweets from the twitter account
        tweets = api.user_timeline(screen_name=twitteraccount, count=4)
        jsontweets =[]
        for tweet in tweets:
            jsontweets.append(json.loads(json.dumps(tweet._json))["text"])
        print(jsontweets)
        for text in jsontweets:
            print(get_tweet_sentiment(text))  #stores the tweets in a json file
            file_object.write(text)
# Tweets are saved in a file in the event of a power failure the data is not lost


query = imput("Which twitter account is used?\n")
number = imput ("How many Tweets should be analyzed?")

results = api.search(
    lang = "en",
    q = query + "-rt",
    count =number,
    result_type = "recent"
)
print("---Gathered Tweets \n")

file_name = "Sentiment_Analysis_of_{}_Tweets.json".format(number, query)

with open(file_name, 'w', newline='') as csvfile:
    csv_writer = csv.DictWriter(
        f = csvfile,
        fieldnames=["Tweet", "Sentiment"]
    )
    csv_writer.writeheader()
    print(" store the last number of tweets in a file so it can be retrieved i the event of a power failure\n")








