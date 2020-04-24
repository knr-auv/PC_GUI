import asyncio,socket, struct
from PyQt5 import QtCore

HEADER = 0
DATA = 1

class connectionHandler(QtCore.QObject):
    
    connectionInfo = QtCore.pyqtSignal(object)
    connectionTerminated = QtCore.pyqtSignal()
    clientConnected = QtCore.pyqtSignal()
    dataReceived = QtCore.pyqtSignal(object)
   
    
    rx_state = HEADER
    tx_ready = True
    tx_buff = []
    
    def __init__(self, addr):
        super(connectionHandler, self).__init__()
        self.host = addr[0]
        self.port = addr[1]
        self.active = True

    

    async def clientHandler(self, reader,writer):
        self.clientConnected.emit()
        self.connectionInfo.emit(("Connected with: "+ str(writer.get_extra_info('peername'))))
        
        rx_len = 0
        try:
            while self.active:
                if len(self.tx_buff)!=0 and self.tx_ready==True:
                    self.tx_ready= False
                    writer.write(self.tx_buff.pop(0))
                    await writer.drain()
                    self.tx_ready=True
                print("abc")
                if(self.rx_state == HEADER):
                    data = await reader.read(4)
                    rx_len = struct.unpack(">L",data)
                    self.rx_state = DATA
                else:
                    try:
                        data = await reader.readexactly(rx_len[0])
                        self.rx_state = HEADER
                        self.dataReceived.emit(data)
                    except asyncio.IncompleteReadError:
                        self.connectionInfo.emit("Message was corrupted")
                        self.rx_state = HEADER

        except ConnectionResetError:
            self.connectionTerminated.emit()
            self.connectionInfo.emit("Client disconnected")
            return

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
    
        
            
    def _send(self, data):
        #protecting buffer 
        self.tx_ready = False
        self.tx_buff.append(data)
        self.tx_ready = True

class parser():

     def send(self, data):
         pass

     def sendPids(P, I, D):
         tx_buffer = [0, P,I,D]
         tx_buffer = struct.pack('<2i3f', *([4+len(tx_buffer)]+tx_buffer))
         self.send(tx_buffer)