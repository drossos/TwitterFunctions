import tweepy
import json
import datetime


#initialization
consumer_key = 'DSKPgaFUZ7q7FVgcrJp3FYEvk'
consumer_secret = 'nMfxwQ44EUwf5UPWTPUZZK83hkxDzDKfS30as2Ipen4AgpMi4k'
access_token = '1131008741736951809-tRDxdJn8XtoevbDgNqagL2W3P66wNU'
access_secret = 'k66MriO3EsDKLeZrdbMpdwrdH5TOpNmosOYCxJEhUuRMU'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)


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