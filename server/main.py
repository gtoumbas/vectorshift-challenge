import asyncio
import uuid

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from kafka_client import KafkaClient


app = FastAPI()
kafka_client = KafkaClient()

@app.on_event("startup")
async def startup_event():
    await kafka_client.start()
    asyncio.create_task(kafka_client.listen_for_messages('results'))  # Start listening for messages


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_client.stop()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    identifier = str(uuid.uuid4())
    inactivity_timeout = 100

    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=inactivity_timeout)
                if data == "close":
                    break
                number = int(data)
                kafka_client.register_websocket(number, websocket, identifier)
                await kafka_client.send_message('numbers', data, identifier)
            except asyncio.TimeoutError:
                await websocket.close()
                break
    except WebSocketDisconnect:
        pass