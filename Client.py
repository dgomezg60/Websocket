import asyncio
import websockets
import random
import time

async def send_authentication_message(client,token):
        struct = r'{{"Token":"{}","ID":"{}"}}'
        FirstMessage = struct.format(token,0)
        await client.send(FirstMessage)

async def listen():
    async with websockets.connect('ws://localhost:8765') as client:
        token = "59"
        await send_authentication_message(client,token)
        try:
            while True:
                # struct = r'{{"IDRobot":"{}","Position":[0,0,0],"Speed":50,"Blocked":true,"Queued":true,"Status":"Enty","ErrorStatus":0,"BatteryLevel":20}}'
                # message = struct.format(7)
                start = time.time()
                # await client.send(f'{message}')
                answer = await client.recv()
                end = time.time()
                print(f"Received: {answer}")
                print(f"Tiempo de respuesta {end-start} s")
                time.sleep(2)
        except websockets.exceptions.ConnectionClosedOK:
            print("Permission denied")
            quit()


if __name__ == "__main__":
    try:
        #Id = random.randint(0,99)
        asyncio.get_event_loop().run_until_complete(listen())
    except websockets.exceptions.ConnectionClosedError:
        print("Connection Error")
    except KeyboardInterrupt:
        print("\nDisconnect")

