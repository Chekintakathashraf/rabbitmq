import pika
import json

def publish_message(message):
    host = 'localhost'
    username = 'guest'
    password = 'guest'
    virtual_host = '/'
    
    credentials = pika.PlainCredentials(username, password)
    
    parameters = pika.ConnectionParameters(
        host=host,
        virtual_host=virtual_host,
        credentials=credentials
    )
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="my_queue")
    message = json.dumps(message)
    channel.basic_publish(
        exchange='',
        routing_key="my_queue",
        body=message
    )
    
    print(f"Message published: {message}")
    connection.close()
