from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

# TODO: Add necessary logic for routing messages to the correct websocket
class KafkaClient:
    def __init__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
        self.consumer = AIOKafkaConsumer(bootstrap_servers='localhost:9092')

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def stop(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def send_message(self, topic: str, message: str):
        await self.producer.send_and_wait(topic, message.encode('utf-8'))

    async def listen_for_messages(self, topic: str):
        self.consumer.subscribe(topic)
        async for msg in self.consumer:
            print(f"Received message: {msg.value.decode('utf-8')}")
            message = msg.value.decode('utf-8')
            number, factors = message.split(':')
            for websocket in self.websocket_map[number]:
                await websocket.send_text(factors)
            del self.websocket_map[number]

    def register_websocket(self, number: int, websocket):
        self.websocket_map[str(number)].append(websocket)