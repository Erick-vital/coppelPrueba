import pika, uuid, json

class RpcClient(object):

    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('host-rabbit'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n
        )
        self.connection.process_data_events(time_limit=None)
        print('enviando..')
        return self.response

# r_client = RpcClient()

#print(" [x] Requesting fib(erick, 1234)")
#response = r_client.call('{"username":"erick", "password":"1234"}')
#print(" [.] Got %r" % response)
# print("{0}".format("{0}".format((response.decode()))))