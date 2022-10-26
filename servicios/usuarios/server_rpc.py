import pika, json
from routers.users import login_for_access_token
from fastapi import Form

connection = pika.BlockingConnection(pika.ConnectionParameters('host-rabbit'))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


# esta es la funcion callback
def on_request(ch, method, props, body):
    # El numero para la serie fibonacci
    # que nos llega desde el cliente
    respuesta = json.loads(body)
    f = Form()
    f.username = respuesta['username']
    f.password = respuesta['password']

    print(" [.] fib(%s)" % respuesta)

    response = login_for_access_token(f)
    token = response['access_token']

    ch.basic_publish(exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id = \
            props.correlation_id),
            body=token
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
# cuando el request es recibo envia la respuesta el callback
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()