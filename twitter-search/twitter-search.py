import os
import tweepy
import csv
import keys
import pandas as pd
####input your credentials here

auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('banktweets.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

search_terms = {'@Chase OR #chasebank', '@BankOfAmerica OR #BankOfAmerica OR @BofA_Help', '@RBC OR #RBC', '@TD_Canada OR #TD', '@Scotiabank OR #scotiabank', '@BMO OR #BMO', '@CIBC OR #cibc'}

for search_term in search_terms:
    for tweet in tweepy.Cursor(api.search,q=search_term, count=100,
                               lang="en",
                               since="2017-04-03").items():
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
        print(tweet.created_at, tweet.text)
