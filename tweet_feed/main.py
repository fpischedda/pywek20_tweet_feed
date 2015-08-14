import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import settings
from producer import Producer


def parse_data(data):
    obj = json.loads(data)

    return {
        'profile_image': obj['user']['profile_image_url'],
        'friends_count': obj['user']['friends_count'],
        'text': obj['text'],
        'favorite_count': obj['favorite_count'],
        'retweet_count': obj['retweet_count'],
        'hashtags': [ht['text'] for ht in obj['entities']['hashtags']]
    }


class Listener(StreamListener):

    def __init__(self, publisher, *args, **kwargs):

        self.publisher = publisher
        super(Listener, self).__init__(*args, **kwargs)

    def on_data(self, data):

        try:
            parsed = parse_data(data)
            self.publisher.send_msg(parsed)
        except Exception as e:
            print("exception: {exception}".format(exception=e))

        return True

    def on_exception(self, exception):
        print(exception)

    def on_error(self, status):
        print("Error occurred, status: {status}".format(status=status))

auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

publisher = Producer(settings.BROKER_URL)
twitterStream = Stream(auth, Listener(publisher))
track = ["#pyweek20", "#pyweek", "#python", "#django", "#mobile"]
twitterStream.filter(track=track, async=True)
