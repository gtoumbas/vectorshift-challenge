import asyncio
import websockets

async def send_numbers(websocket, numbers):
    for number in numbers:
        await websocket.send(str(number))
        print(f"Sent: {number}")

async def receive_responses(websocket, identifier, count):
    for _ in range(count):
        response = await websocket.recv()
        print(f"Response to {identifier}: {response}")

async def handle_websocket(uri, numbers, identifier, batch_send):
    async with websockets.connect(uri) as websocket:
        if batch_send:
            sender_task = asyncio.create_task(send_numbers(websocket, numbers))
            receiver_task = asyncio.create_task(receive_responses(websocket, identifier, len(numbers)))
            await sender_task
            await receiver_task
        else:
            for number in numbers:
                await websocket.send(str(number))
                print(f"Sent from {identifier}: {number}")
                response = await websocket.recv()
                print(f"Response to {identifier}: {response}")

async def main():
    uri = "ws://localhost:8000/ws"
    test_numbers_1 = [
        16,
        66706930041755363083,
        111906709554793344173,
        28049854149491043631,
    ]
    test_numbers_2 = [
        1016669087450202913,
        3211891798434562153,
    ]
    task1 = asyncio.create_task(handle_websocket(uri, test_numbers_1, "WebSocket 1", True))
    task2 = asyncio.create_task(handle_websocket(uri, test_numbers_2, "WebSocket 2", False))
    await asyncio.gather(task1, task2)

asyncio.run(main())
