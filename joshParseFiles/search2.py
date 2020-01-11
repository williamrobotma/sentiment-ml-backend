import tweepy
import csv
import keys
import pandas as pd
import os
####input your credentials here


auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
search_terms = ('@RBC OR #RBC')
csvFile = open('rbc.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,q=search_terms,count=1000,
                           lang="en",
                           since="2017-04-03").items():
    if (not tweet.retweeted) and ('RT @' not in tweet.text):
        # print (tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
