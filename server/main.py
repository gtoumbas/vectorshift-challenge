from fastapi import FastAPI, WebSocket

from kafka_client import KafkaClient


app = FastAPI()
kafka_client = KafkaClient()


@app.on_event("startup")
async def startup_event():
    await kafka_client.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_client.stop()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "close":
            break
        number = int(data)
        # TODO: Send number to prime factorizer through Kafka
        # TODO: Send the prime factors back to the client through the websocket once complete
        # TODO: After 5 seconds of inactivity (e.g., no outstanding tasks), close the websocket
