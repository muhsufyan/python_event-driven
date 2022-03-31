import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
# # simple publisher
# def publish():
#     channel.basic_publish(exchange='', routing_key='admin', body="hallo fastapi")
#     channel.basic_publish(exchange='', routing_key='flask', body="hallo flask")

# method adlah event yg dikirim sprti product_created yg diterima dari app/main.py /createProduct, sedangkan body adlh data yg dikirim dari app/main.py /createProduct
# keduanya dikirim lewat publish() di app/main.py /createProduct
def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='flask', body=json.dumps(body), properties=properties)