import pika
import pandas as pd
import json
import uuid

def generateExcel(message):
    message = json.loads(message)
    df = pd.DataFrame(message)
    filename = f"output_{uuid.uuid4()}.xlsx"
    df.to_excel(filename, index=False)
    print(f"Excel file generated: {filename}")

def callback(ch, method, properties, body):
    message = body.decode()
    generateExcel(message)

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
channel.basic_consume(queue="my_queue", on_message_callback=callback, auto_ack=True)
print("Consumer started...")
channel.start_consuming()
