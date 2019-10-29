# This is Part C
import tweepy #Twitter API
from tweepy import Stream #establishes streaming session
from tweepy import OAuthHandler #authentication handler
from tweepy.streaming import StreamListener #classify most common twitter messages and routes them to appropriately named methods
import json # readable format for structuring data
import time # analysis of time
import os #operating system dependent functionalities
from textblob import TextBlob #library for processing textual data (NLP)
import sys  # provides access to some variables used or maintained by the interpreter
import re #specifies a set of strings that matches it
import pandas as pd #handling data
import numpy as np #for the computing of numbers

#for plotting and visualization purposes:
from IPython.display import display
import matplotlib.pyplot as plt #visualization library
import seaborn as sns #visualization library based on matplotlib
%matplotlib inline

#user credentials to access Twitter API
consumer_key="ReElT98AQjypB3ci6jddzj6zi"
consumer_secret="P2miZKpbDhydB2lp8OlZvQUVHB2lW7cS9Px3bI9Xv0M4i8bist"
access_token="975795800134574080-MsFAepUwuaVBYc71skhORVEUimSTEOp"
access_token_secret="w2DPJhuJjvc0RwmYbKyFzK6Zmb2jkb29behisyawcrU5B"

#get authentication and initialization of  tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#checking every minute the number of tweets on a twitter account
twitteraccount = "realdonaldtrump"
user = api.get_user(twitteraccount)
# print Twitter account name and the number of followers
tweets = extractor.user_timeline(screen_name="realdonaldtrump", count=300)
print("Number_of_tweets extracted:{}".format(len(tweets)))
print("screen_name: " + user.screen_name)
print("Number of followers: " + str(user.followers_count))
print("Following" + str(user.friends_count))
print("location: " + user.location)

file_object= open("tweets.json", "w")


def clean_tweet(tweet):  #only tweet text is allowed

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ /  \ /  \S+)", " ", tweet).split())  #removes links or special characters and emojis

def get_tweet_sentiment(tweet): #analysis of passed tweets
    # object of passed tweet text created
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment for the pibrella lights
    if analysis.sentiment.polarity > 0:
        pibrella.light.green.on()
        return 'positive'

    elif analysis.sentiment.polarity == 0:
        pibrella.light.amber.on()
        return 'neutral'
    else:
        pibrella.light.red.on()
        return 'negative'

oldtime = time.time()  #view of the actual time
while True:    #program obtains the latest four tweets
    if (time.time() -oldtime > 59) or pibrella.button.pressed():
        oldtime = time.time()
        number_of_tweets = user.statuses_count
        # Retrieve the last four tweets from the twitter account
        tweets = api.user_timeline(screen_name=twitteraccount, count=4)
        jsontweets =[]
        for tweet in tweets:
            jsontweets.append(json.loads(json.dumps(tweet._json))["text"])
        print(jsontweets)
        for text in jsontweets:
            print(get_tweet_sentiment(text))    #stores the tweets in a json file
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
    print(" store the last number of tweets in a file so it can be retrieved in the event of a power failure\n")
#Part E1 is written in Part C because the above code is needed to do the following:
#Source: Sentiment analysis from Rudolfo Ferro
#creating dataframe
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

#The first 15 elements are displayed in the dataframe
display(data.head(15))

#adding some data such as Date, Likes and Source

data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['len'] = np.array([len(tweet.text) for tweet in tweets])
data['Likes'] = np.array([tweet.favourite_count for tweet in tweets])

#The first 15 elements are displayed in the dataframe
display(data.head(15))

#average length of a Trump tweet
mean = np.mean(data['len'])
print("The average length of a twitter tweet:{}".format(mean))

#analysis of likes and retweets
fav_max = np.max(data['Likes'])
rt_max = np.max(data['RTs'])  #number of Retweets

fav = data[data.Likes == fav_max].index[0]
rt = data[data.RTs == rt_max].index[0]

#favourite Twitter tweets in terms of likes
print("The tweet with more likes is: \n{{".format(data['Tweets'][fav]))
print("Number of the likes:{}".format(fav_max))
print("{}characters.\n".format(data['len'][fav]))
print("{}characters.\n".format(data['len'][fav]))

#favourite Twitter retweets
print("The highest retweet is:\n{}".format(data['Tweets'][rt]))
print("The number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))

#creating a time series with tweets lengths, likes and retweets
tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

#tweet lengths visualization
tlen.plot(figsize=15,4), color= "red");
tfav.plot(figsize=15,4), label="Likes", legend=True)
tret.plot(figsize=15,4), label="Retweets", legend=True);


#result of the sentiment analysis
data['SA'] = np.array([analyze_sentiment(tweet) for tweet in data['Tweets']])
#displaying the dataframe
display(data.head(10))
#classifying tweets according to their sentiments
positive_tweets = [tweet for index, tweet in enumerate(data['Tweets']) if data ['SA'][index] > 0]
#print the percentage of tweets with a positive sentiment
print("Percentage of tweets viewed positive: {}%".format(len(postive_tweets)*100/len(data['Tweets'])))
neutral_tweets = [tweet for index, tweet in enumerate(data['Tweets']) if data ['SA'][index] == 0]
#print the percentage of tweets with a neutral sentiment
print("Percentage of tweets viewed neutral: {}%".format(len(neutral_tweets)*100/len(data['Tweets'])))
negative_tweets = [tweet for index, tweet in enumerate(data['Tweets']) if data ['SA'][index] < 0]
#print the percentage of tweets with a negative sentiment
print("Percentage of tweets viewed negative: {}%".format(len(negative_tweets)*100/len(data['Tweets'])))