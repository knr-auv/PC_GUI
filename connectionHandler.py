import asyncio,socket, struct
from PyQt5 import QtCore



class connectionHandler(QtCore.QObject):
    
    connectionInfo = QtCore.pyqtSignal(object)
    connectionTerminated = QtCore.pyqtSignal()
    clientConnected = QtCore.pyqtSignal()
    dataReceived = QtCore.pyqtSignal(object)
    HEADER = 0
    DATA = 1
  
    
    def __init__(self, addr):
        super(connectionHandler, self).__init__()
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
        self.rx_state = self.HEADER
        self.tx_ready = True
        self.tx_buff = []
    

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
                
                if(self.rx_state == self.HEADER):
                    data = await reader.readexactly(4)
                    rx_len = struct.unpack("<L",data)[0]
                    rx_len -= 4
                    self.rx_state = self.DATA
                else:
                    try:
                        data = await reader.readexactly(rx_len)
                        data = struct.unpack("<5I",data)
                        self.dataReceived.emit(data)
                        print(data)
                        self.rx_state = self.HEADER
                        
                    except asyncio.IncompleteReadError:
                        self.connectionInfo.emit("Message was corrupted")
                        self.rx_state = self.HEADER

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
        asyncio.run(self.serverHandler(),debug =True)
    #TODO terminate all active connection before closing
    def stop(self):
        self.server.close()
        if self.server.is_serving():
            print("Server is runnig --> we have a problem")
    
        
            
    def send(self, data):
        #protecting buffer 
        self.tx_ready = False
        self.tx_buff.append(data)
        self.tx_ready = True

class parser():
    def __init__(self, func):
        self.send=func

    def sendPids(P, I, D):
        tx_buffer = [0, P,I,D]
        tx_buffer = struct.pack('<2i3f', *([4+len(tx_buffer)]+tx_buffer))
        self.send(tx_buffer)
