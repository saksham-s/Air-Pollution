from __future__ import print_function
import tweepy
import json
import pymongo
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
app = Flask(__name__)
from pymongo import MongoClient
client=MongoClient()
db=client.twitterdb
import numpy as np
from afinn import Afinn

# hashtag task
# Pollution
tweets_iterator1 = db.pollution.find()
hashtags_frequency1={}
for tweet in tweets_iterator1:
	for i in tweet['entities']['hashtags']:
		# print(i['text'].lower())
		if(str(i['text'].encode('utf-8')).lower() in hashtags_frequency1):
			hashtags_frequency1[str(i['text'].encode('utf-8')).lower()]+=1
		else:
			hashtags_frequency1[str(i['text'].encode('utf-8')).lower()]=1
hashtags_frequency1= sorted(hashtags_frequency1.items(), key=lambda x:x[1])
hashtag_frequency1=hashtags_frequency1[-10:]
cat1=["#"+i[0] for i in hashtag_frequency1]
hashtags_frequency1=[i[1] for i in hashtag_frequency1]

# Rains
tweets_iterator2 = db.rains.find()
hashtags_frequency2={}
for tweet in tweets_iterator2:
	for i in tweet['entities']['hashtags']:
		if(str(i['text'].encode('utf-8')).lower() in hashtags_frequency2):
			hashtags_frequency2[str(i['text'].encode('utf-8')).lower()]+=1
		else:
			hashtags_frequency2[str(i['text'].encode('utf-8')).lower()]=1
hashtags_frequency2= sorted(hashtags_frequency2.items(), key=lambda x:x[1])
hashtag_frequency2=hashtags_frequency2[-10:]
cat2=["#"+i[0] for i in hashtag_frequency2]
hashtags_frequency2=[i[1] for i in hashtag_frequency2]




# retweet vs original tweets
# Pollution
tweets_iterator1 = db.pollution.find()
original1=0
retweets1=0
for tweet in tweets_iterator1:
	if("retweeted_status" in tweet):
		retweets1+=1
	else:
		original1+=1
part6_pollution1=[["Original",original1],["Retweets",retweets1]]

# Rains
tweets_iterator2 = db.rains.find()
original2=0
retweets2=0
for tweet in tweets_iterator2:
	if("retweeted_status" in tweet):
		retweets2+=1
	else:
		original2+=1
part6_pollution2=[["Original",original2],["Retweets",retweets2]]

# Geo location
# Pollution
tweets_iterator1 = db.pollution.find()
loc1=[]
for tweet in tweets_iterator1:
	if(tweet["coordinates"] is not None):
		user1=tweet["user"]["screen_name"]
		lon1 = tweet["coordinates"]['coordinates'][0]
		lat1 = tweet["coordinates"]['coordinates'][1]
		loc1.append([lat1,lon1,str(user1)])

# Rains
tweets_iterator2 = db.rains.find()
loc2=[]
for tweet in tweets_iterator2:
	if(tweet["coordinates"] is not None):
		user2=tweet["user"]["screen_name"]
		lon2 = tweet["coordinates"]['coordinates'][0]
		lat2 = tweet["coordinates"]['coordinates'][1]
		loc2.append([lat2,lon2,str(user2)])


# Distribution of tweets
# Pollution
tweets_iterator1 = db.pollution.find()
text1=0
image1=0
text_image1=0
for tweet in tweets_iterator1:
	if("media" in tweet['entities'] and (("text" in tweet) and tweet['text'])):	
		text_image1+=1
	elif("media" in tweet['entities']):
		image1+=1
	elif(("text" in tweet) and tweet['text']):
		text1+=1
distribution1=[["Text",text1],["Image",image1],["Text & Image",text_image1]]

# Rains
tweets_iterator2 = db.rains.find()
text2=0
image2=0
text_image2=0
for tweet in tweets_iterator2:
	if("media" in tweet['entities'] and (("text" in tweet) and tweet['text'])):	
		text_image2+=1
	elif("media" in tweet['entities']):
		image2+=1
	elif(("text" in tweet) and tweet['text']):
		text2+=1
distribution2=[["Text",text2],["Image",image2],["Text & Image",text_image2]]


# Favourite Count
# Pollution
tweets_iterator1 = db.pollution.find()
favourite_count_frequency1=[]
for tweet in tweets_iterator1:
	if("retweeted_status" in tweet):
		pass
	elif float(tweet['favorite_count']) <20:
		favourite_count_frequency1.append([float(tweet['favorite_count'])])

# Rains
tweets_iterator2 = db.rains.find()
favourite_count_frequency2=[]
for tweet in tweets_iterator2:
	if("retweeted_status" in tweet):
		pass
	elif float(tweet['favorite_count']) <20:
		favourite_count_frequency2.append([float(tweet['favorite_count'])])


# Non-region users currently for non delhi
# Pollution
tweets_iterator1 = db.pollution.find()
dates1=[]
for tweet in tweets_iterator1:
	a=tweet["created_at"].encode('utf-8').split(" ")
	date=a[1]+" "+a[2]+" "+a[5]
	if(date not in dates1):
		dates1.append(date)
dates_freq1=np.zeros(len(dates1))

tweets_iterator1 = db.pollution.find()
for tweet in tweets_iterator1:
	if(not(tweet["user"]["location"]=="") and ("delhi" not in str(tweet['user']['location'].encode('utf-8')).lower())):
		for i in range(0,len(dates1)):
			a=tweet["created_at"].encode('utf-8').split(" ")
			if(str(dates1[i])==str(a[1]+" "+a[2]+" "+a[5])):
				dates_freq1[i]+=1

# Rains
tweets_iterator2 = db.rains.find()
dates2=[]
for tweet in tweets_iterator2:
	a=tweet["created_at"].encode('utf-8').split(" ")
	date=a[1]+" "+a[2]+" "+a[5]
	if(date not in dates2):
		dates2.append(date)
dates_freq2=np.zeros(len(dates2))

tweets_iterator2 = db.rains.find()
for tweet in tweets_iterator2:
	if(not(tweet["user"]["location"]=="") and ("mumbai" not in str(tweet['user']['location'].encode('utf-8')).lower()) 
		and ("bombay" not in str(tweet['user']['location'].encode('utf-8')).lower())):
		for i in range(0,len(dates2)):
			a=tweet["created_at"].encode('utf-8').split(" ")
			if(str(dates2[i])==str(a[1]+" "+a[2]+" "+a[5])):
				dates_freq2[i]+=1



# Network Graph
# Pollution
tweets_iterator1 = db.pollution.find()
indegree1={}
outdegree1={}

for tweet in tweets_iterator1:
	if("retweeted_status" in tweet):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["retweeted_status"]["user"]["screen_name"]
		temp["type"]="Reply"	
		if(temp["source"] in outdegree1):
			outdegree1[temp["source"]]+=1
		else:
			outdegree1[temp["source"]]=1
		if(temp["target"] in indegree1):
			indegree1[temp["target"]]+=1
		else:
			indegree1[temp["target"]]=1

	if("user_mentions" in tweet["entities"]):
		for user in tweet["entities"]["user_mentions"]:
			temp={}
			temp["source"]=tweet["user"]["screen_name"]
			temp["target"]=user["screen_name"]
			temp["type"]="Reply"
			if(temp["source"] in outdegree1):
				outdegree1[temp["source"]]+=1
			else:
				outdegree1[temp["source"]]=1

			if(temp["target"] in indegree1):
				indegree1[temp["target"]]+=1
			else:
				indegree1[temp["target"]]=1


	if(tweet["in_reply_to_screen_name"] is not None):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["in_reply_to_screen_name"]
		temp["type"]="Reply"
		if(temp["source"] in outdegree1):
			outdegree1[temp["source"]]+=1
		else:
			outdegree1[temp["source"]]=1
		if(temp["target"] in indegree1):
			indegree1[temp["target"]]+=1
		else:
			indegree1[temp["target"]]=1

tweets_iterator1 = db.pollution.find()
graph1_mention=[]
graph1_retweet=[]
graph1_reply=[]
for tweet in tweets_iterator1:
	if("retweeted_status" in tweet):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["retweeted_status"]["user"]["screen_name"]
		temp["type"]="Reply"
		sum1=0
		sum2=0
		if(temp["source"] in outdegree1):
			sum1+=outdegree1[temp["source"]]
		if(temp["source"] in indegree1):
			sum1+=indegree1[temp["source"]]
		if(temp["target"] in outdegree1):
			sum2+=outdegree1[temp["target"]]
		if(temp["target"] in indegree1):
			sum2+=indegree1[temp["target"]]
		if(sum1>10 and sum2>10):
			graph1_retweet.append(temp)

	if("user_mentions" in tweet["entities"]):
		for user in tweet["entities"]["user_mentions"]:
			temp={}
			temp["source"]=tweet["user"]["screen_name"]
			temp["target"]=user["screen_name"]
			temp["type"]="Reply"
			sum1=0
			sum2=0
			if(temp["source"] in outdegree1):
				sum1+=outdegree1[temp["source"]]
			if(temp["source"] in indegree1):
				sum1+=indegree1[temp["source"]]
			if(temp["target"] in outdegree1):
				sum2+=outdegree1[temp["target"]]
			if(temp["target"] in indegree1):
				sum2+=indegree1[temp["target"]]
			if(sum1>10 and sum2>10):
				graph1_mention.append(temp)

	if(tweet["in_reply_to_screen_name"] is not None):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["in_reply_to_screen_name"]
		temp["type"]="Reply"
		if(temp["source"] in outdegree1):
			sum1+=outdegree1[temp["source"]]
		if(temp["source"] in indegree1):
			sum1+=indegree1[temp["source"]]
		if(temp["target"] in outdegree1):
			sum2+=outdegree1[temp["target"]]
		if(temp["target"] in indegree1):
			sum2+=indegree1[temp["target"]]
		if(sum1>5 and sum2>5):
			graph1_reply.append(temp)

graph1_reply=json.dumps(graph1_reply)
graph1_mention=json.dumps(graph1_mention)
graph1_retweet=json.dumps(graph1_retweet)


# Rains
tweets_iterator2 = db.rains.find()
indegree2={}
outdegree2={}

for tweet in tweets_iterator2:
	if("retweeted_status" in tweet):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["retweeted_status"]["user"]["screen_name"]
		temp["type"]="Reply"	
		if(temp["source"] in outdegree2):
			outdegree2[temp["source"]]+=1
		else:
			outdegree2[temp["source"]]=1
		if(temp["target"] in indegree2):
			indegree2[temp["target"]]+=1
		else:
			indegree2[temp["target"]]=1

	if("user_mentions" in tweet["entities"]):
		for user in tweet["entities"]["user_mentions"]:
			temp={}
			temp["source"]=tweet["user"]["screen_name"]
			temp["target"]=user["screen_name"]
			temp["type"]="Reply"
			if(temp["source"] in outdegree2):
				outdegree2[temp["source"]]+=1
			else:
				outdegree2[temp["source"]]=1

			if(temp["target"] in indegree2):
				indegree2[temp["target"]]+=1
			else:
				indegree2[temp["target"]]=1


	if(tweet["in_reply_to_screen_name"] is not None):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["in_reply_to_screen_name"]
		temp["type"]="Reply"
		if(temp["source"] in outdegree2):
			outdegree2[temp["source"]]+=1
		else:
			outdegree2[temp["source"]]=1
		if(temp["target"] in indegree2):
			indegree2[temp["target"]]+=1
		else:
			indegree2[temp["target"]]=1

tweets_iterator2 = db.rains.find()
graph2_mention=[]
graph2_retweet=[]
graph2_reply=[]
for tweet in tweets_iterator2:
	if("retweeted_status" in tweet):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["retweeted_status"]["user"]["screen_name"]
		temp["type"]="Reply"
		sum1=0
		sum2=0
		if(temp["source"] in outdegree2):
			sum1+=outdegree2[temp["source"]]
		if(temp["source"] in indegree2):
			sum1+=indegree2[temp["source"]]
		if(temp["target"] in outdegree2):
			sum2+=outdegree2[temp["target"]]
		if(temp["target"] in indegree2):
			sum2+=indegree2[temp["target"]]
		if(sum1>20 and sum2>20):
			graph2_retweet.append(temp)

	if("user_mentions" in tweet["entities"]):
		for user in tweet["entities"]["user_mentions"]:
			temp={}
			temp["source"]=tweet["user"]["screen_name"]
			temp["target"]=user["screen_name"]
			temp["type"]="Reply"
			sum1=0
			sum2=0
			if(temp["source"] in outdegree2):
				sum1+=outdegree2[temp["source"]]
			if(temp["source"] in indegree2):
				sum1+=indegree2[temp["source"]]
			if(temp["target"] in outdegree2):
				sum2+=outdegree2[temp["target"]]
			if(temp["target"] in indegree2):
				sum2+=indegree2[temp["target"]]
			if(sum1>20 and sum2>20):
				graph2_mention.append(temp)

	if(tweet["in_reply_to_screen_name"] is not None):
		temp={}
		temp["source"]=tweet["user"]["screen_name"]
		temp["target"]=tweet["in_reply_to_screen_name"]
		temp["type"]="Reply"
		if(temp["source"] in outdegree2):
			sum1+=outdegree2[temp["source"]]
		if(temp["source"] in indegree2):
			sum1+=indegree2[temp["source"]]
		if(temp["target"] in outdegree2):
			sum2+=outdegree2[temp["target"]]
		if(temp["target"] in indegree2):
			sum2+=indegree2[temp["target"]]
		if(sum1>5 and sum2>5):
			graph2_reply.append(temp)
			
graph2_reply=json.dumps(graph2_reply)
graph2_mention=json.dumps(graph2_mention)
graph2_retweet=json.dumps(graph2_retweet)

# Sentiment analysis
# Pollution
afinn = Afinn(emoticons=True)
tweets_iterator1 = db.pollution.find()
count_positive1=0
count_negative1=0
count_neutral1=0
for tweet in tweets_iterator1:
	if(afinn.score(tweet['text'].encode('utf-8'))>0):
		count_positive1+=1
	elif(afinn.score(tweet['text'].encode('utf-8'))==0):
		count_neutral1+=1
	else:
		count_negative1+=1
sent1=[]
names1=["Positive","Negative","Neutral"]
val1=[count_positive1,count_negative1,count_neutral1]
for i in range(0,3):
	sent1.append([names1[i],val1[i]])

# Rains
tweets_iterator2 = db.rains.find()
count_positive2=0
count_negative2=0
count_neutral2=0
for tweet in tweets_iterator2:
	if(afinn.score(tweet['text'].encode('utf-8'))>0):
		count_positive2+=1
	elif(afinn.score(tweet['text'].encode('utf-8'))==0):
		count_neutral2+=1
	else:
		count_negative2+=1
sent2=[]
names2=["Positive","Negative","Neutral"]
val2=[count_positive2,count_negative2,count_neutral2]
for i in range(0,3):
	sent2.append([names2[i],val2[i]])

# # ec2-13-115-54-217.ap-northeast-1.compute.amazonaws.com 13.115.54.217
@app.route("/")
def contentpage():
	return render_template("index.html")

@app.route("/top10/pollution")
def top10pollution():
	return render_template("top10.html",cat=cat1,hashtags_frequency=hashtags_frequency1)

@app.route("/top10/rains")
def top10rains():
	return render_template("top10.html",cat=cat2,hashtags_frequency=hashtags_frequency2)

@app.route("/originalvsretweet/pollution")
def originalvsretweetpollution():
	return render_template("originalvsretweet.html",input=part6_pollution1)

@app.route("/originalvsretweet/rains")
def originalvsretweetrains():
	return render_template("originalvsretweet.html",input=part6_pollution2)

@app.route("/geolocations/pollution")
def geolocationspollution():
	return render_template("geoloc.html",loc=loc1)

@app.route("/geolocations/rains")
def geolocationsrains():
	return render_template("geoloc.html",loc=loc2)

@app.route("/distributionoftweets/pollution")
def distributionoftweetspollution():
	return render_template("distributionoftweets.html",dist=distribution1)

@app.route("/distributionoftweets/rains")
def distributionoftweetsrains():
	return render_template("distributionoftweets.html",dist=distribution2)

@app.route("/favourite/pollution")
def favouritepollution():
	return render_template("favourite.html",fav=favourite_count_frequency1)

@app.route("/favourite/rains")
def favouriterains():
	return render_template("favourite.html",fav=favourite_count_frequency2)

@app.route("/nonregion/pollution")
def nonregionpollution():
	return render_template("nonregion.html",dates=dates1,dates_freq=dates_freq1.tolist())

@app.route("/nonregion/rains")
def nonregionrains():
	return render_template("nonregion.html",dates=dates2,dates_freq=dates_freq2.tolist())

@app.route("/sentiment/pollution")
def sentimentpollution():
	return render_template("sentiment.html",sent=sent1)

@app.route("/sentiment/rains")
def sentimentrains():
	return render_template("sentiment.html",sent=sent2)

@app.route("/network/pollution/mention")
def networkpollutionmention():
	return render_template("network.html",graph=graph1_mention)

@app.route("/network/pollution/retweet")
def networkpollutionretweet():
	return render_template("network.html",graph=graph1_retweet)

@app.route("/network/pollution/reply")
def networkpollutionreply():
	return render_template("network.html",graph=graph1_reply)

@app.route("/network/rains/mention")
def networkrainsmention():
	return render_template("network.html",graph=graph2_mention)


@app.route("/network/rains/retweet")
def networkrainsretweet():
	return render_template("network.html",graph=graph2_retweet)

@app.route("/network/rains/reply")
def networkrainsreply():
	return render_template("network.html",graph=graph2_reply)

if __name__ == "__main__":
	app.run()