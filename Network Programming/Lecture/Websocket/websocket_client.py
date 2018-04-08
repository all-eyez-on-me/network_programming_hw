import asyncio
import websockets
async def hello():
    async with websockets.connect('ws://localhost:50001') as websocket:
        name = 'Albert'
        await websocket.send(name)
        print("Sent: {}".format(name))
        msg = await websocket.recv()
        print("Received: {}".format(msg))
asyncio.get_event_loop().run_until_complete(hello())