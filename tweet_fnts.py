import tweepy
import json
import datetime
import tweet_auth_creds as tac

#initialization

auth = tweepy.OAuthHandler(tac.consumer_key, tac.consumer_secret)
auth.set_access_token(tac.access_token, tac.access_secret)


api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#publicTweets = api.home_timeline()

def get_followers(usname):
    user = api.get_user(usname)
    followers = list()

    for friend in user.friends():
        followers.append(friend.screen_name)
    
    return(followers)

def save_tweets(usname):
    user = api.get_user(usname)
    #Large amount of user tweets
    tweets = tweepy.Cursor(api.user_timeline, id = usname, include_rts = False, tweet_mode = 'extended').items()

    #itterate through and save the tweets to txt for training
    with open('data/user_tweets.txt', 'w', encoding='utf8') as out:
        out.truncate(0)
        for tweet in tweets:
                out.write(tweet.full_text)
                out.write("\n")
        

save_tweets("realDonaldTrump")