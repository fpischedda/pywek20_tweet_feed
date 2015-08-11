import pika
import ujson


class Consumer:

    EXCHANGE_NAME = 'feed_source'
    EXCHANGE_TYPE = 'fanout'

    def __init__(self, amqp_url):

        if amqp_url is not None:
            self.connect(amqp_url)
        else:
            self.connect = None

    def connect(self, amqp_url):

        print("connecting...")
        self.connection = pika.BlockingConnection(
            pika.URLParameters(amqp_url)
        )

        self.channel = self.connection.channel()
        # self.channel.exchange_declare(self.EXCHANGE_NAME,
        #                               self.EXCHANGE_TYPE,
        #                               passive=False,
        #                               durable=False,
        #                               auto_delete=True)
        self.queue = self.channel.queue_declare(exclusive=True).method.queue
        self.channel.queue_bind(exchange=self.EXCHANGE_NAME,
                                queue=self.queue,
                                routing_key='/')

    def start_consuming(self):

        print("start consuming...")
        self.channel.basic_consume(self.consume_callback,
                                   queue=self.queue,
                                   no_ack=True)
        try:
            self.channel.start_consuming()
        finally:
            self.close_connection()

    def consume_callback(self, ch, method, properties, body):
        print("callback body:{body}".format(body=body))
        self.on_message(ujson.loads(body))

    def on_message(self, msg):
        print(msg)

    def close_connection(self):
        self.connection.close()


if __name__ == '__main__':

    consumer = Consumer('amqp://guest:guest@localhost:5672/%2F')
    consumer.start_consuming()
    consumer.close_connection()
