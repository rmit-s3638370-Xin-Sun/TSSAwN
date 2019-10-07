from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s

# TODO replace the local database with cloud database
# import MySQLdb
#                         server        MySQL username	MySQL pass  Database name.
# conn = MySQLdb.connect("mysql.server","beginneraccount","cookies","beginneraccount$tutorial")
# c = conn.cursor()

# twitter streaming API
# consumer key, consumer secret, access token, access secret.
secret = []
with open("secret.txt", "r") as f:
    for line in f.readlines():
        secret.append(line.strip())

ckey = str(secret[0])
csecret = str(secret[1])
atoken = str(secret[2])
asecret = str(secret[3])


class TweetsListener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]

        # username = all_data["user"]["screen_name"]
        # c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)", (time.time(), username, tweet))
        # conn.commit()

        sentiment_value, confidence = s.sentiment(tweet)
        print(tweet, sentiment_value, confidence)

        if confidence * 100 >= 80:
            output = open("twitter-out.txt", "a")
            output.write(sentiment_value)
            output.write('\n')
            output.close()

        return True

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

target = "Joaquin Phoenix"
twitterStream = Stream(auth, TweetsListener())
twitterStream.filter(track=[target])
