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
    inactivity_timeout = 5

    kafka_client.register_websocket(websocket, identifier)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=inactivity_timeout)
                if data == "close":
                    break
                await kafka_client.send_message('numbers', data, identifier)
            except asyncio.TimeoutError:
                # Close if no pending messages
                if kafka_client.get_pending_messages(identifier) == 0:
                    await websocket.close()
                    kafka_client.unregister_websocket(identifier)
                    break

    except WebSocketDisconnect:
        pass