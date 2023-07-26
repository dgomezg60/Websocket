import asyncio
from time import sleep
import websockets
import json

ClientAuthorised = {}

async def authenticate(FirstMessage,client):
    message = json.loads(FirstMessage)
    if message['Token'] == "59":
        authenticated = True
        ClientAuthorised[message['ID']] = client
    else:
        authenticated = False
    if authenticated:
        return True
    else:
        return False

async def diconect(client):
    await client.close()
    print(f'Client disconected {client.id}')
    try:
        _ = ClientAuthorised.pop(list(ClientAuthorised.keys())[list(ClientAuthorised.values()).index(client)])
    except ValueError:
        pass

##-------------------------------------------------------------------Server listen----------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async def read_message(client):
    text = await client.recv()
    message = json.loads(text)
    print("ID:{}, Position: {}".format(message['IDRobot'],message['Position']))

async def server_handler_listen(client):
    authenticated = False
    auth_message = await client.recv()
    authenticated = await authenticate(auth_message,client)
    if authenticated:
        try:
            print(f'Client conected {client.id}')
            while True:
                await read_message(client)
        except websockets.exceptions.ConnectionClosed:
            await diconect(client)
    else:
        await client.close()

##-------------------------------------------------------------------Server send----------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async def send_message(Id):
    try:
        client = ClientAuthorised[f'{Id}']
        struct = r'{{"IDRobot":"{}","Position":[10,20,60]}}'
        message = struct.format(Id)
        print(client)
        await client.send(message)
    except KeyError:
        print(f'Cliend with ID {Id} doesnt exist')

async def server_handler_send(client):
    authenticated = False
    auth_message = await client.recv()
    authenticated = await authenticate(auth_message,client)
    if authenticated:
        print(f'Client conected {client.id}')
        try:
            while len(ClientAuthorised) != 0:
                    await send_message(0)
                    sleep(1)
        except websockets.exceptions.ConnectionClosed:
            await diconect(client)
    else:
        await client.close()

##------------------------------------------------------------------- Main ----------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async def start_server(Ports):
    server = await websockets.serve(server_handler_send, 'localhost', Ports[0])
    print(f'Sending server turn on, at localhost:{Ports[0]}')
    ListeningServer = await websockets.serve(server_handler_listen, 'localhost', Ports[1])
    print(f'Listening server turn on, at localhost:{Ports[1]}')
    await server.wait_closed()

if __name__ == '__main__':
    Ports = [8765,8766]
    try:
        asyncio.run(start_server(Ports))
    except KeyboardInterrupt:
        print('\nServer turn off')
    except TimeoutError:
        print('\nDisconect out of time')
