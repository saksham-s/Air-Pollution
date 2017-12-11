from __future__ import print_function
import tweepy
import json
import pymongo
from pymongo import MongoClient
client=MongoClient()
db=client.twitterdb

access_token="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_key="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

MAX_TWEETS=20000
oldest1=0
count=0
query="%23Smog%20OR%20%23SmogInDelhi%20OR%20%23delhiAirpollution%20OR%20%23MyRightToBreathe%20OR%20%23CropBurning%20OR%20%23delhipollution%20OR%20%23DelhiinSmog%20OR%20%23DelhiSmog%20OR%20%23DelhiChokes%20OR%20%23letdelhibreathe%20OR%20%23rightobreathe%20OR%20%23pollutionindelhi"
while(count<MAX_TWEETS):
	try:
		if(oldest1<=0):
			tweets_array=api.search(q=query,count=100,include_rts=True,include_entities=True,lang="en")
		else:
			tweets_array=api.search(q=query,count=100,max_id=str(oldest1-1),include_rts=True,include_entities=True,lang="en")
		for tweet in tweets_array:
			db.pollution.insert(tweet._json)
			count+=1
			oldest1=tweet.id
			print(count)
	except:
		print(oldest1)
		print ("some error: ")
		break

access_token="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_key="XXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret="XXXXXXXXXXXXXXXXXXXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

MAX_TWEETS=20000
oldest2=0
count=0
query="%23MumbaiRains%20OR%20%23CycloneOckhi%20OR%20%23Ockhi%20OR%20%23CycloneOkhi%20OR%20%23cyclone"
while(count<MAX_TWEETS):
	try:
		if(oldest2<=0):
			tweets_array=api.search(q=query,count=100,include_rts=True,include_entities=True,lang="en")
		else:
			tweets_array=api.search(q=query,count=100,max_id=str(oldest2-1),include_rts=True,include_entities=True,lang="en")
		for tweet in tweets_array:
			db.rains.insert(tweet._json)
			count+=1
			oldest2=tweet.id
			print(count)

	except:
		print(oldest2)
		print ("some error:")
		break
