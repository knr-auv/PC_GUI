import asyncio,socket
from PyQt5 import QtCore

class connectionHandler(QtCore.QObject):
    connectionInfo = QtCore.pyqtSignal(object)
   
    connectionTerminated = QtCore.pyqtSignal()
    clientConnected = QtCore.pyqtSignal()
    dataReceived = QtCore.pyqtSignal(object)

    def __init__(self, addr):
        super(connectionHandler, self).__init__()

        self.host = addr[0]
        self.port = addr[1]
        self.active = True

    async def clientHandler(self, reader,writer):
        self.clientConnected.emit()
        self.connectionInfo.emit(("Connected with: "+ str(writer.get_extra_info('peername'))))
        
        try:
            while self.active:
                data = await reader.read(100)
                if not data == b'':
                    self.dataReceived.emit(data)
                else:
                    break
        except ConnectionResetError:
            self.connectionTerminated.emit()
            self.connectionInfo.emit("Client disconnected")
            return


           
            
        #writer.write(data)
        #await writer.drain()
        
        writer.close()
        
        await writer.wait_closed()
        return

    async def serverHandler(self):
        self.server = await asyncio.start_server(self.clientHandler, self.host, self.port, family = socket.AF_INET, flags = socket.SOCK_STREAM)
        self.connectionInfo.emit("Server is listening: " + str(self.host)+":"+str(self.port))
        
        try:
           async with self.server:
                await self.server.serve_forever()
       
        except asyncio.CancelledError:
            self.active=False
            self.connectionInfo.emit("Server terminated")
            await self.server.wait_closed()
            


           
    def run(self):
        asyncio.run(self.serverHandler())

    def stop(self):
        self.server.close()
        if self.server.is_serving():
            print("Server is runnig --> we have a problem")
       
        
            
       
   