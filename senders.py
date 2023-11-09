import time

import pika


class RabbitMqConfig:
    def __init__(self, queue='one', exchange='', routing_key='one', body='hi', host='localhost'):
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key
        self.body = body
        self.host = host


class RabbitMq:
    def __init__(self, server):
        self.server = server
        self._connection = pika.BlockingConnection(parameters=pika.ConnectionParameters(host=self.server.host))
        self.chanel = self._connection.channel()

    def sending(self):
        self.chanel.queue_declare(queue=self.server.queue)
        for i in range(4):
            print('sending...')
            time.sleep(2)

        self.chanel.basic_publish(exchange=self.server.exchange, routing_key=self.server.routing_key,
                                  body=self.server.body)
        time.sleep(6)
        self._connection.close()


if __name__ == '__main__':
    body = str(input('Enter password: '))

    server1 = RabbitMqConfig(queue='two', routing_key='two', body=body)
    rab1 = RabbitMq(server1)
    rab1.sending()
