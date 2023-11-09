import pika
import hashlib
import uuid
import senders
import base64

connections = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))

ch = connections.channel()

ch.queue_declare(queue='two')


def collback(ch, method, properties, body):
    print('hashing...')
    old_password = body
    salt = uuid.uuid4().hex
    password = hashlib.md5(old_password).hexdigest()
    conf = senders.RabbitMqConfig(body=f"{body}  ====  {password}")
    rab = senders.RabbitMq(conf)
    rab.sending()
    print("done")


print('waiting for messages, for exit (ctl+c)')

ch.basic_consume(queue='two', on_message_callback=collback, auto_ack=True)

ch.start_consuming()
