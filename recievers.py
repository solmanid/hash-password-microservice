import pika

connections = pika.BlockingConnection(parameters=pika.ConnectionParameters(host='localhost'))

ch = connections.channel()

ch.queue_declare(queue='one')


def collback(ch, method, properties, body):
    print('start...')
    f = open('password.txt', 'a')
    f.write(f"{body}\n")
    f.close()
    print('You can see hashed password in "password.txt" file.')
    print('done!')


print('waiting for messages, for exit (ctl+c)')

ch.basic_consume(queue='one', on_message_callback=collback, auto_ack=True)

ch.start_consuming()
