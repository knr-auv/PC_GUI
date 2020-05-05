import asyncio,socket, struct, threading
from PyQt5 import QtCore



class connectionHandler(QtCore.QObject):
    #TODO deal with mess in signals
    connectionInfo = QtCore.pyqtSignal(object)
    connectionStatus = QtCore.pyqtSignal(object)
    connectionTerminated = QtCore.pyqtSignal()
    dataReceived = QtCore.pyqtSignal(object)
    
    def __init__(self, addr):
        super(connectionHandler, self).__init__()
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
            
    async def client(self):
        
        self.connectionInfo.emit(("Connecting to: "+ str(self.host)+":"+str(self.port)))
        try:
            self.connectionStatus.emit("Connecting...")
            reader, self.writer = await asyncio.open_connection(host = self.host, port = self.port, family = socket.AF_INET, flags = socket.SOCK_STREAM)
        except ConnectionRefusedError:
            self.connectionInfo.emit("Connection refused")
            self.connectionStatus.emit("Connect")
            return
        self.client_loop = asyncio.get_running_loop()
        self.connectionInfo.emit(("Connected with: "+ str(self.writer.get_extra_info('peername'))))
        self.connectionStatus.emit("Disconnect")
        HEADER = 0
        DATA = 1
        rx_state = HEADER
        rx_len =0
        try:
            while self.active:    
                try:
                    if(rx_state ==HEADER):
                        async def receive4():
                            data = await reader.readexactly(4)
                            return data
                        self.reader_task = asyncio.create_task(receive4())  #there should be another way to stop reading task...
                        data = await self.reader_task
                        rx_len = struct.unpack("<L",data)[0]
                        rx_len -= 4
                        rx_state = DATA

                    elif(rx_state == DATA):
                        data = await reader.readexactly(rx_len)
                        data = struct.unpack("<5I",data)
                        print(data)
                        rx_state = HEADER                            
                except asyncio.IncompleteReadError:
                    rx_state = HEADER
                except asyncio.CancelledError:
                    pass
        except ConnectionResetError:
            self.reader_task.cancel()
            self.connectionInfo.emit("Connection terminated")
            self.connectionStatus.emit("Connect")
            self.connectionTerminated.emit()
            return
        self.writer.close()
        await self.writer.wait_closed()
        self.connectionInfo.emit("Connection terminated")
        self.connectionStatus.emit("Connect")
       
    def run(self):
        asyncio.run(self.client(), debug = True)
        
    def stop(self):
        async def coro():
            self.reader_task.cancel() 
        self.active = False
        try:
            asyncio.run_coroutine_threadsafe(coro(), self.client_loop)
        except AttributeError:
            pass
        
          
    def send(self, data):
        async def write():
            self.writer.write(data)
            await self.writer.drain()       
        asyncio.run_coroutine_threadsafe(write(), self.client_loop)

class parser():
    def __init__(self, func):
        self.send=func

    def sendPids(P, I, D):
        tx_buffer = [0, P,I,D]
        tx_buffer = struct.pack('<2i3f', *([4+len(tx_buffer)]+tx_buffer))
        self.send(tx_buffer)
