import tweepy #Twitter API
from tweepy import Stream #establishes streaming session
from tweepy import OAuthHandler  #authentication handler
from tweepy.streaming import StreamListener  #classify most common twitter messages and routes them to appropriately named methods
import json # readable format for structuring data
import time # analysis of time
from textblob import TextBlob #library for processing textual data (NLP)


#user credentials Twitter API
consumer_key="ReElT98AQjypB3ci6jddzj6zi"
consumer_secret="P2miZKpbDhydB2lp8OlZvQUVHB2lW7cS9Px3bI9Xv0M4i8bist"
access_token="975795800134574080-MsFAepUwuaVBYc71skhORVEUimSTEOp"
access_token_secret="w2DPJhuJjvc0RwmYbKyFzK6Zmb2jkb29behisyawcrU5B"

#authentication and initialisation of  tweepy
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

