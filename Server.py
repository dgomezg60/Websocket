import asyncio
import websockets
import json

##-------------------------------------------------------------------Authentication Server----------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async def authenticate(FirstMessage,client,typ):
    message = json.loads(FirstMessage)
    if message['Token'] == "59":
        authenticated = True
        if typ == 1:
            ClientAuthorisedListener[message['ID']] = client
        if typ == 2:
            ClientAuthorisedSender[message['ID']] = client
    else:
        authenticated = False
    if authenticated:
        return True
    else:
        return False

async def disconect(client):
    await client.close()
    print(f'Client disconected {client.id}')
    try:
        _ = ClientAuthorisedSender.pop(list(ClientAuthorisedSender.keys())[list(ClientAuthorisedSender.values()).index(client)])
        _ = ClientAuthorisedListener.pop(list(ClientAuthorisedListener.keys())[list(ClientAuthorisedListener.values()).index(client)])
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
    authenticated = await authenticate(auth_message,client,1)
    if authenticated:
        try:
            print(f'Client conected {client.id}')
            while True:
                await read_message(client)
        except websockets.exceptions.ConnectionClosed:
            await disconect(client)
    else:
        await client.close()

##-------------------------------------------------------------------Server sender----------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async def send_message(Id):
    try:
        client = ClientAuthorisedSender[f'{Id}']
        struct = r'{{"IDRobot":"{}","Position":[0,0,0]}}'
        message = struct.format(Id)
        await client.send(message)
        await asyncio.sleep(0.02)
    except KeyError:
        print(f'Cliend with ID {Id} doesnt exist')

async def server_handler_send(client):
    authenticated = False
    auth_message = await client.recv()
    authenticated = await authenticate(auth_message,client,2)
    if authenticated:
        print(f'Client conected {client.id}')
        try:
            while len(ClientAuthorisedSender) != 0:
                print('Do you want send a message? [y/n]')
                Answer = input()
                if Answer == 'y':
                    await send_message(0)
        except websockets.exceptions.ConnectionClosed:
            await disconect(client)
    else:
        await client.close()

##------------------------------------------------------------------- Main ----------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async def WaitClosed(Server):
    await Server.wait_closed()

async def start_server(Ports):
    global Ip
    server = await websockets.serve(server_handler_send, Ip, Ports[0])
    print(f'Sending server turn on, at {Ip}:{Ports[0]}')
    ListeningServer = await websockets.serve(server_handler_listen, Ip , Ports[1])
    print(f'Listening server turn on, at {Ip}:{Ports[1]}')
    await asyncio.gather(WaitClosed(server),WaitClosed(ListeningServer))

if __name__ == '__main__':
    Ports = [8765,8766]
    Ip = '192.168.0.16'
    ClientAuthorisedSender = {}
    ClientAuthorisedListener = {}
    try:
        asyncio.run(start_server(Ports))
    except KeyboardInterrupt:
        print('\nServer turn off')
    except TimeoutError:
        print('\nDisconect out of time')
