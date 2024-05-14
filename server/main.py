from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
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
    inactivity_timeout = 5

    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=inactivity_timeout)
                if data == "close":
                    break
                number = int(data)
                kafka_client.register_websocket(number, websocket)
                await kafka_client.send_message('numbers', data)
            except asyncio.TimeoutError:
                await websocket.close()
                break
    except WebSocketDisconnect:
        pass