import asyncio
from time import sleep
import websockets
import json

class client():
    def __init__(self,Identify):
        self.Id = Identify

    async def __SendAuthenticationMessage(self):
        struct = r'{{"Token":"{}","ID":"{}"}}'
        FirstMessage = struct.format(self.token,self.Id)
        await self.__clientListener.send(FirstMessage)
        #await self.__clientSender.send(FirstMessage)

    async def connected(self,Token):     
        try:
            self.__clientListener = await websockets.connect(f'ws://localhost:8765')
            #self.__clientSender = await websockets.connect(f'ws://localhost:8766')
            self.token = Token
            await self.__SendAuthenticationMessage()
        except websockets.exceptions.ConnectionClosedError:
            print("\nConnection Error")
        except KeyboardInterrupt:
            print("\nDisconnect")

    async def SendParameters(self,Position,Speed,Blocked,Queued,Status,ErrorStatus,BatteryLevel):
    #async def SendParameters(self):
        #struct = r'{{"IDRobot":"{}","Position":[0,0,0],"Speed":50,"Blocked":true,"Queued":true,"Status":"Enty","ErrorStatus":0,"BatteryLevel":20}}'
        struct  = r'{{"IDRobot":"{}","Position":"{}","Speed":"{}","Blocked":"{}","Queued":"{}","Status":"{}","ErrorStatus":"{}","BatteryLevel":"{}"}}'
        message = struct.format(self.Id,Position,Speed,Blocked,Queued,Status,ErrorStatus,BatteryLevel)
        message = struct.format(self.Id)
        await self.__clientSender.send(message)

    async def ListeningServer(self):
        Order = await self.__clientListener.recv()
        self.message = json.loads(Order)
        print("ID:{}, Position: {}".format(self.message['IDRobot'],self.message['Position']))
        print(self.__clientListener)
        sleep(1)
        await self.ListeningServer()

async def main():
    Amr = client(0)
    await Amr.connected("59")
    try:
        #await Amr.SendParameters()
        await Amr.ListeningServer()
    except KeyboardInterrupt:
        print('Disconnect')
        quit()
    except websockets.exceptions.ConnectionClosedError:
        print('Unathenticated')

if __name__ == '__main__':
    asyncio.run(main())
