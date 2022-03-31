import pika, json
from main import db, Product
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='flask')

def callback(ch, method, properties, body):
    print("data diterima dari flask")
    # print(body)
    data = json.loads(body)
    print(data)
    if properties.content_type == 'product_created':
        product = Product(id=data['id'],title=data['title'],image=data['image'])
        db.session.add(product)
        db.session.commit()
        print(product)
        print('product created')
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['data']['title']
        product.image = data['data']['image']
        db.session.commit()
        print(product)
        print('product update')
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        print(product)
        db.session.delete(product)
        db.session.commit()
        print('product delete')
channel.basic_consume(queue='flask', on_message_callback=callback, auto_ack=True)
print("start consuming")
channel.start_consuming()

channel.close()