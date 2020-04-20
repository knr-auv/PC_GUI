import asyncio,socket
from PyQt5 import QtCore

class connectionHandler(QtCore.QObject):
    
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
        addr = writer.get_extra_info('peername')
        print("connected with ", addr)
        
        while self.active:
            
            data = await reader.read(100)
            
            if not data == b'':
                self.dataReceived.emit(data)
            else:
                break
           
            
            #writer.write(data)
            #await writer.drain()
        self.connectionTerminated.emit()
        writer.close()
        print("terminated")
        await writer.wait_closed()
        return

    async def serverHandler(self):
        self.server = await asyncio.start_server(self.clientHandler, self.host, self.port, family = socket.AF_INET, flags = socket.SOCK_STREAM)
        print("server started on: ", self.server.sockets[0].getsockname())
        try:
           async with self.server:
                await self.server.serve_forever()
        except asyncio.CancelledError:
            self.active=False
            await self.server.wait_closed()
            


           
    def run(self):
        asyncio.run(self.serverHandler())

    def stop(self):
        self.server.close()
        if not self.server.is_serving():
            print("Server closed")
       
        
            
       
   