#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy                   # Python wrapper around Twitter API
from datetime import date
from datetime import datetime
import time
import keys


# In[2]:


api_key = keys.api_key
api_secret_key = keys.api_secret_key
access_token = keys.access_token
access_token_secret = keys.access_token_secret
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[3]:


def limit_handled(cursor, list_name):
    """Function to catch the tweepy api rate limit"""
    while True:
        try:
            yield cursor.next()    # Catch Twitter API rate limit exception and wait for 15 minutes
        except tweepy.RateLimitError:
            print("\nData points in list = {}".format(len(list_name)))
            print('Hit Twitter API rate limit.')
            for i in range(3, 0, -1):
                print("Wait for {} mins.".format(i * 5))
                time.sleep(5 * 60)    # Catch any other Twitter API exceptions
        except tweepy.error.TweepError:
            print('\nCaught TweepError exception' )
        except StopIteration:
            break
            
#function to get tweets
def get_all_tweets_info(handle):
    """Gets the follwing information from a twitter account number of likes,number of retweets,number of tweets"""
    alltweets = []  
    new_tweets = api.user_timeline(screen_name = handle,count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1 
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))    # all subsequent requests use the max_id param to prevent
        # duplicates
        new_tweets = api.user_timeline(screen_name = handle,count=200,max_id=oldest)    # save most recent tweets
        alltweets.extend(new_tweets)    # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(alltweets)))
    tweets_list = []
    likes = []
    retweet_count = []
    
    for tweet in alltweets:
        tweets_text = tweet.text
        tweets_likes = tweet.favorite_count
        tweets_retweeted = tweet.retweeted

        
        tweets_list.append(tweets_text)
        likes.append(tweets_likes)
        retweet_count.append(tweets_retweeted)
        
    return len(tweets_list),sum(likes),sum(retweet_count)
    
def followers_count(handle):
    """ Determines the number of followers for a given twitter account"""
  
    followers_list = []
    cursor = tweepy.Cursor(api.followers,screen_name=handle,count=200).pages()
    print("loading followers number")
    for i, page in enumerate(limit_handled(cursor, followers_list)):  

        # Add latest batch of follower data to the list
        followers_list += page
    follower_count = len(followers_list)
    return follower_count

def following_count(handle):
    """Determines the number of people following a given twitter account"""
    following_list = []
    cursor = tweepy.Cursor(api.friends,screen_name=handle,count=200).pages()
    print("Loading following numbers")
    for i,page in enumerate(limit_handled(cursor, following_list)):
        following_list += page
    friends_count = len(following_list)
    return friends_count


# In[4]:


#followers_count("okiomagerald")


# In[5]:


#following_count("okiomagerald")


# In[6]:


#type(get_all_tweets_info("okiomagerald"))


# In[7]:


import pandas as pd
data_tweets = pd.DataFrame(columns=['Handle','N_tweets','N_likes','N_retweeted','N_followed','N_following'])


# In[8]:


influencers = pd.read_csv('data.csv')


# In[9]:


influencers=influencers[['username','twitter_handle']]
influencers['twitter_handle']= influencers['twitter_handle'].str.strip(')')
influencers.head()


# In[ ]:


index = 1
for i in influencers['twitter_handle']:
    handle = i
    tweets_count,likes_count,retweets_count = get_all_tweets_info(handle)
    count_no_followers = followers_count(handle)
    count_no_following = following_count(handle)
    user_data = [handle,tweets_count,likes_count,retweets_count,count_no_followers,count_no_following]
    data_tweets.loc[index]=user_data
    print(data_tweets)
    if index == 100:
        data_tweets.to_csv("batch1.csv")
    if index == 200:
        data_tweets.to_csv("batch2.csv")
    if index == 300:
        data_tweets.to_csv("batch3.csv")
    if index == 400:
        data_tweets.to_csv("batch4.csv")
    if index == 500:
        data_tweets.to_csv("batch5.csv")
    if index == 600:
        data_tweets.to_csv("batch6.csv")
    index += 1


# In[ ]:


data_tweets.head()


# In[ ]:





# In[ ]:




