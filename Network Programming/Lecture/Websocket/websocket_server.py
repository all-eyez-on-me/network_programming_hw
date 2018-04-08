import asyncio
import websockets
async def handle(websocket, path):
    name = await websocket.recv()
    print("Received: {}".format(name))
    msg = "Hello {}!".format(name)
    await websocket.send(msg)
    print("Sent: {}".format(msg))
start_server = websockets.serve(handle, 'localhost', 50001)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.run_forever()