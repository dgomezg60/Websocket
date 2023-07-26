import asyncio
import time
import websockets
import json

class client():
    def __init__(self,Identify):
        self.Id = Identify

    async def __SendAuthenticationMessage(self):
        struct = r'{{"Token":"{}","ID":"{}"}}'
        FirstMessage = struct.format(self.token,self.Id)
        await asyncio.gather(self.__clientListener.send(FirstMessage),self.__clientSender.send(FirstMessage))
        # await self.__clientListener.send(FirstMessage)
        # await self.__clientSender.send(FirstMessage)

    async def connected(self,Token):     
        try:
            self.__clientListener = await websockets.connect(f'ws://192.168.0.16:8765')
            self.__clientSender = await websockets.connect(f'ws://192.168.0.16:8766')
            self.token = Token
            await self.__SendAuthenticationMessage()
        except websockets.exceptions.ConnectionClosedError:
            print("\nConnection Error")
        except KeyboardInterrupt:
            print("\nDisconnect")

    #async def SendParameters(self,Position,Speed,Blocked,Queued,Status,ErrorStatus,BatteryLevel):
    async def SendParameters(self):
        while True:
            struct = r'{{"IDRobot":"{}","Position":[0,0,0],"Speed":50,"Blocked":true,"Queued":true,"Status":"Enty","ErrorStatus":0,"BatteryLevel":20}}'
            #struct  = r'{{"IDRobot":"{}","Position":"{}","Speed":"{}","Blocked":"{}","Queued":"{}","Status":"{}","ErrorStatus":"{}","BatteryLevel":"{}"}}'
            #message = struct.format(self.Id,Position,Speed,Blocked,Queued,Status,ErrorStatus,BatteryLevel)
            message = struct.format(self.Id)
            await self.__clientSender.send(message)
            await asyncio.sleep(1)


    async def ListeningServer(self):
        while True:
            print('Escucho')
            Order = await self.__clientListener.recv()
            self.message = json.loads(Order)
            print("ID:{}, Position: {}".format(self.message['IDRobot'],self.message['Position']))

async def main():
    Amr = client(0)
    print('Me conecto')
    await Amr.connected("59")
    try:
        await asyncio.gather(Amr.SendParameters(),Amr.ListeningServer())
    except KeyboardInterrupt:
        print('Disconnect')
        quit()
    except websockets.exceptions.ConnectionClosedError:
        print('Unathenticated')

if __name__ == '__main__':
    asyncio.run(main())
