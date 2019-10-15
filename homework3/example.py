import GetOldTweets3 as got
import re

tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama")\
    .setTopTweets(True)\
    .setMaxTweets(10)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)[4]

string1 = "is"
count1 = 0
print(type(tweet.text))
print(tweet.text)
t = tweet.text
print(t.count(string1))
