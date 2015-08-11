Tweet Feed
==========

Tweet Feed is a simple application that uses the Twitter's streaming api in 
order to feed data to my pyweek20 entry.

All tweets are parsed and sent as json to an AMQP fan out exchange, game
clients binds a queue the the exchange in order to use the streaming data and
create game entities.

Running the demon
-----------------

Prerequisites:
- an AMQP broker for example RabbitMQ
- twitter app credentials (create an app on Twitter to get consumer and access
  credentials)
- create a .env file using .env.example as a base 
- install dependencies using pip install -r requirements.txt (use tools such as
  virtualenv to create a clean working environment)

Running the service:
- run python main.py 
- if you inspect the rabbitmq web console you should see some traffic on
  feed_source exchange
