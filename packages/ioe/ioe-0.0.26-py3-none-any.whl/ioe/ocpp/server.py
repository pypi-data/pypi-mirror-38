import asyncio
import websockets


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

print('Serving OCPP on 0.0.0.0 port 8765 (ws://0.0.0.0:8765/) ...')
asyncio.get_event_loop().run_until_complete(websockets.serve(echo,
                                                             '0.0.0.0',
                                                             8765))
asyncio.get_event_loop().run_forever()
