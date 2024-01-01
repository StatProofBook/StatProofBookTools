#!/usr/bin/env python
"""
Tweet Random Proof from the StatProofBook
_
This script tweets one random proof from the StatProofBook per day,
without repetition within a year, and then:
- opens the tweet from the current day (in a webbrowser)
- reports a summary for the current year.

Author: Joram Soch, BCCN Berlin
E-Mail: joram.soch@bccn-berlin.de

First edit: 2022-12-29 17:17:00
 Last edit: 2023-08-23 15:15:00
"""


# Import modules
#-----------------------------------------------------------------------------#
import os
import json
import random
import tweepy
import webbrowser
import BookTools as spbt
from datetime import datetime, timedelta

# Set repository directory
#-----------------------------------------------------------------------------#
rep_dir = spbt.get_rep_dir('offline')

# Retrieve Twitter API keys
#-----------------------------------------------------------------------------#
file_obj = open(rep_dir + '/../' + 'TwitterAPIKeys.json')
api_dict = json.load(file_obj)
api_key       = api_dict['api_key']
api_secret    = api_dict['api_key_secret']
access_token  = api_dict['access_token']
access_secret = api_dict['access_token_secret']
bearer_token  = api_dict['bearer_token']

# Authorize Twitter access
#-----------------------------------------------------------------------------#
client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_secret)
user   = client.get_me() # equivalent solution:
# user = client.get_user(username=api_dict['username'])

# List files in proof directory
#-----------------------------------------------------------------------------#
files  = os.listdir(rep_dir + '/P/')
files  = [file for file in files if not file.startswith('-temp-')]
proofs = []

# Browse through list of files
#-----------------------------------------------------------------------------#
for file in files:
    
    # Read proof text
    #-------------------------------------------------------------------------#
    file_obj = open(rep_dir + '/P/' + file, 'r')
    file_txt = file_obj.readlines()
    file_obj.close()
    
    # Get proof info
    #-------------------------------------------------------------------------#
    proof_id, shortcut, title, username, date = spbt.get_meta_data(file_txt)
    proofs.append({'proof_id': proof_id, 'shortcut': shortcut, 'title': title, \
                   'username': username, 'date': date})

# Collect eligible tweets and randomize
#-----------------------------------------------------------------------------#
dt = datetime.today()
yt = dt.year
d0 = datetime(yt, 1, 1)
proofs = [proof for proof in proofs if proof['date']<d0]
random.seed(yt)
random.shuffle(proofs)

# Create schedule for current year
#-----------------------------------------------------------------------------#
schedule = []
date     = d0
while date.year == yt:
    
    # schedule proof/tweet
    #-------------------------------------------------------------------------#
    i = (date-d0).days
    schedule.append((i+1, date, proofs[i]))
    
    # show today's tweet
    #-------------------------------------------------------------------------#
    if date.date() == dt.date():
        print('\nDay {}: {}: the tweet reads:\n'.format(i+1, date.strftime('%A, %B %d, %Y')))
        tweet_text = 'Proof #{}: "{}" ({}) #RandomProof\nhttps://statproofbook.github.io/P/{}'
        tweet_text = tweet_text.format(proofs[i]['proof_id'][1:], proofs[i]['title'], \
                                       proofs[i]['shortcut'], proofs[i]['shortcut'])
        print(tweet_text)
        
    # change to next day
    #-------------------------------------------------------------------------#
    date = date + timedelta(days=1)

# Prepare for working off schedule
#-----------------------------------------------------------------------------#
num_days  = 0
num_tweet = 0
rem_tweet = 0
tweet_msg = ['not sent', 'sent']
Forbidden = False
print()

# Cycle through schedule
#-----------------------------------------------------------------------------#
for i, date, proof in schedule:
    
    # if the day was already there
    #-------------------------------------------------------------------------#
    if date.date() <= dt.date():
           
        # show message for this day
        print('Day {}: {}: '.format(i, date.strftime('%A, %B %d, %Y')), end='')
        num_days = num_days + 1
        
        # create and fill tweet text
        tweet_text = 'Proof #{}: "{}" ({}) #RandomProof\nhttps://statproofbook.github.io/P/{}'
        tweet_text = tweet_text.format(proof['proof_id'][1:], proof['title'], \
                                       proof['shortcut'], proof['shortcut'])
        end_pos    = tweet_text.find('#RandomProof')+len('#RandomProof')
        
        # retrieve tweets from this day
        try:
            tweets = client.get_users_tweets(user.data.id, max_results=100, \
                                             start_time=date, end_time=date+timedelta(days=1))
            tweets = tweets.data
        except tweepy.errors.Forbidden:
            print('the request has been forbidden!')
            Forbidden = True
            break
                        
        # go through tweets to check if sent
        #---------------------------------------------------------------------#
        tweet_sent = False
        if tweets != None:
            for tweet in tweets:
                if tweet.text[:end_pos] == tweet_text[:end_pos]:
                    tweet_sent = True
                    num_tweet  = num_tweet + 1
                    # if day is today, store tweet for later
                    if date.date() == dt.date(): tweet_today = tweet
        
        # if day already passed: report status
        #---------------------------------------------------------------------#
        if date.date() < dt.date():            
            
            # display status message
            print('the tweet was {}.'.format(tweet_msg[int(tweet_sent)]))
            
        # if day is today: release new tweet
        #---------------------------------------------------------------------#
        if date.date() == dt.date():
            
            # if tweet was sent, say it was already sent
            if tweet_sent:
                print('the following tweet was already sent:')
            
            # if tweet was not sent, send tweet for today
            else:
                tweet = client.create_tweet(text=tweet_text, user_auth=True)
                print('the following tweet was posted:')
                # since day is today, store tweet for later
                tweet_today = tweet.data
                num_tweet   = num_tweet + 1
            
            # display tweet details
            tweet_msg = '\nUser "{}", Status {}:\n»{}«'
            print(tweet_msg.format(user.data.username, tweet_today['id'], tweet_today['text']))
            
            # open tweet webpage
            tweet_url = 'https://twitter.com/{}/status/{}'
            webbrowser.open(tweet_url.format(user.data.username, tweet_today['id']))
    
    # if the day is still to come
    #-------------------------------------------------------------------------#
    else:
        
        # count remaining tweets
        rem_tweet = rem_tweet + 1
        
# Display final report
#-----------------------------------------------------------------------------#
if not Forbidden:
    print('\nSummary for year {}:'.format(yt))
    print('- scheduled tweets: {}'.format(len(schedule)))
    print('- days passed: {}'.format(num_days))
    print('- tweets sent: {}'.format(num_tweet))
    print('- days to come: {}'.format(rem_tweet))