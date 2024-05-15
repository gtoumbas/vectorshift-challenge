from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

class KafkaClient: 
    def __init__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
        self.consumer = AIOKafkaConsumer(bootstrap_servers='localhost:9092')
        self.websocket_map = {} # (key = identifier, value = {'websocket': websocket, 'pending_messages': int})

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def stop(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def send_message(self, topic: str, message: str, identifier: str):
        self.websocket_map[identifier]['pending_messages'] += 1
        identifier = identifier.encode('utf-8')
        await self.producer.send_and_wait(topic, message.encode('utf-8'), headers=[("ws-identifier", identifier)])

    async def listen_for_messages(self, topic: str):
        self.consumer.subscribe([topic])
        async for msg in self.consumer:
            identifier = dict(msg.headers).get('ws-identifier').decode('utf-8')
            original_with_factors = msg.value.decode('utf-8')
            if identifier in self.websocket_map:
                await self.websocket_map[identifier]['websocket'].send_text(original_with_factors)
                self.websocket_map[identifier]['pending_messages'] -= 1

    
    def register_websocket(self, websocket, identifier: str):
        if identifier not in self.websocket_map:
            self.websocket_map[identifier] = {'websocket': websocket, 'pending_messages': 0}

    def unregister_websocket(self, identifier: str):
        if identifier in self.websocket_map:
            del self.websocket_map[identifier]

    def get_pending_messages(self, identifier: str):
        if identifier in self.websocket_map:
            return self.websocket_map[identifier]['pending_messages']
        else:
            return 0
