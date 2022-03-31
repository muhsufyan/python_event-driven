import pika, json
from app.database import get_references
from app.models import Product

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print("data diterima")
    id = json.loads(body)
    print(id)
    db = get_references()
    cari_id = db.query(Product).filter(Product.id == id)
    product = db.query(Product).filter(Product.id == id).first()
    product.like = product.like + 1
    print('title :{0}, id :{1}, image : {2}, like :{3}, created at :{4}'.format(product.title, product.id, product.image, product.like, product.created_at) )
    cari_id.update({'title':product.title, 'id':product.id, 'image':product.image, 'like':product.like, 'created_at':product.created_at}, synchronize_session=False)
    # simpan ke db
    db.commit()
    print("produk di like")

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print("start consuming")
channel.start_consuming()

channel.close()