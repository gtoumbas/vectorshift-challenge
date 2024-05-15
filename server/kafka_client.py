from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

# TODO: Add necessary logic for routing messages to the correct websocket
class KafkaClient:
    def __init__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
        self.consumer = AIOKafkaConsumer(bootstrap_servers='localhost:9092')
        self.websocket_map = {}

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def stop(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def send_message(self, topic: str, message: str, identifier: str):
        identifier = identifier.encode('utf-8')
        await self.producer.send_and_wait(topic, message.encode('utf-8'), headers=[("ws-identifier", identifier)])

    async def listen_for_messages(self, topic: str):
        self.consumer.subscribe([topic])
        async for msg in self.consumer:
            print(f"Received message: {msg.value.decode('utf-8')}")
            print(f"Message headers: {msg.headers}")
            identifier = dict(msg.headers).get('ws-identifier').decode('utf-8')
            message = msg.value.decode('utf-8')
            factors = message.split(':')
            print(f"Received message: {msg.value} with identifier: {identifier}")

            if identifier in self.websocket_map:
                await self.websocket_map[identifier].send_text(factors)
                # del self.websocket_map[identifier]
          
    
    def register_websocket(self, number: int, websocket, identifier: str):
        print(f"Registering websocket {identifier} for number {number}.")
        if identifier not in self.websocket_map:
            self.websocket_map[identifier] = websocket

