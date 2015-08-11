import pika
import ujson


class Producer:

    EXCHANGE_NAME = 'feed_source'
    EXCHANGE_TYPE = 'fanout'

    def __init__(self, amqp_url=None):

        if amqp_url is not None:
            self.connect(amqp_url)
        else:
            self.connection = None

        self.properties = pika.BasicProperties('application/json')

    def connect(self, amqp_url):

        self.connection = pika.BlockingConnection(
            pika.URLParameters(amqp_url)
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.EXCHANGE_NAME,
                                      self.EXCHANGE_TYPE,
                                      passive=False,
                                      durable=True,
                                      auto_delete=True)

    def send_msg(self, msg_obj):

        self.channel.basic_publish(exchange=self.EXCHANGE_NAME,
                                   routing_key='/',
                                   body=ujson.dumps(msg_obj),
                                   properties=self.properties
                                   )

    def close_connection(self):
        self.connection.close()
