import asyncio,socket, struct, threading, logging

from PyQt5 import QtCore
from concurrent.futures import ThreadPoolExecutor

class odroidClientSignals(QtCore.QObject):
    receivedPID = QtCore.pyqtSignal(object)
    receivedMotors = QtCore.pyqtSignal(object)
    receivedBoatData = QtCore.pyqtSignal(object)
    connectionInfo = QtCore.pyqtSignal(object)
    connectionButton = QtCore.pyqtSignal(object)
    connectionTerminated = QtCore.pyqtSignal()
    connectionRefused = QtCore.pyqtSignal()
    clientConnected = QtCore.pyqtSignal()

class parser():
    ERROR = 0
    PID = 1
    MOTORS = 2
    BOAT_DATA = 3
    def parse(self, data):
        try:
            if data[0]== self.PID:
                ROLL = 1
                PITCH = 2
                YAW = 3
                ALL = 4
                if data[1]!= ALL:
                    msg = struct.unpack('<2B3f', data)
                    msg = list(msg)
                    msg.pop(0)
                    if msg[0]==ROLL:
                        msg[0] = 'roll'
                    elif msg[0]==PITCH:
                        msg[0] ='pitch'
                    elif msg[0]==YAW:
                        msg[0]='yaw'
                    self.signals.receivedPID.emit(msg)
                elif data[1]==ALL:
                    msg  = struct.unpack('<2B9f', data)
                    msg = list(msg)
                    msg.pop(0)
                    msg[0]='all'
                    self.signals.receivedPID.emit(msg)
            elif data[0]==self.MOTORS:
                msg = struct.unpack('<B5f', data)
                msg = list(msg)
                msg.pop(0)
                self.signals.receivedMotors.emit(msg)

            elif data[0] == self.BOAT_DATA:
                msg = struct.unpack('<B5f',data)
                msg = list(data)
                msg.pop(0)
                self.signals.receivedBoatData.emit(msg)
        except:
            sys.exc_info()
            logging.critical("error while parsing data")

class sender():
    CONTROL = 0
    SEND_PID = 1
    PID_REQUEST = 2
    def send(self):
        pass

    def send_msg(self, msg):
        header = struct.pack('<i', len(msg)+4)
        msg = bytearray(header+msg)
        self.send(msg)

    def sendPID(self, PID = []):
        spec = int()
        axis = PID[0]
        if axis=='roll':
            spec=1
        elif axis =='pitch':
            spec = 2
        elif axis == 'yaw':
            spec = 3
        elif axis =='all':
            spec = 4
        else:
            logging.debug(str(axis)+"is not a valid argument of sendPid. Valid arguments: 'roll', 'pitch', 'yaw', 'all'")
            return

        PID.pop(0)
        if spec != 4:
            tx_buffer = [self.SEND_PID,spec]  + PID
            tx_buffer = struct.pack('<2B3f', *(tx_buffer))
            self.send_msg(tx_buffer)
        elif spec == 4:
            tx_buffer = [self.SEND_PID,spec]  + PID
            tx_buffer = struct.pack('<2B9f', *(tx_buffer))
            self.send_msg(tx_buffer)

    def sendControl(self, msg):
        START_SENDING = 1
        if msg[0] == START_SENDING:
            tx_buffer = [self.CONTROL]+msg
            tx_buffer = struct.pack('<2Bf',*(tx_buffer))
            self.send_msg(tx_buffer)

    def sendPIDRequest(self, axis):
        spec = int()
        try:
            if axis=='roll':
                spec=1
            elif axis =='pitch':
                spec = 2
            elif axis == 'yaw':
                spec = 3
            elif axis =='all':
                spec = 4
            else:
                raise invalidValue
        except invalidValue:
            loging.debug(str(axis)+"is not a valid argument of sendPidRequest. Valid arguments: 'roll', 'pitch', 'yaw', 'all'")
        tx_buffer = [self.PID_REQUEST,spec]
        tx_buffer = struct.pack('<2B',*(tx_buffer))
        self.send_msg(tx_buffer)


class odroidClient(QtCore.QRunnable, parser,sender):
    def __init__(self, addr):
        super(odroidClient, self).__init__()
        self.signals = odroidClientSignals()
        #self.parser = parser()
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
            
    async def client(self):
        self.signals.connectionInfo.emit(("Connecting to: "+ str(self.host)+":"+str(self.port)))
        try:
            self.signals.connectionButton.emit("Connecting...")
            reader, self.writer = await asyncio.open_connection(host = self.host, port = self.port, family = socket.AF_INET, flags = socket.SOCK_STREAM)
        except ConnectionRefusedError:
            self.signals.connectionInfo.emit("Connection refused")
            self.signals.connectionButton.emit("Connect")
            self.signals.connectionRefused.emit()
            return
        self.client_loop = asyncio.get_running_loop()
        self.signals.connectionInfo.emit(("Connected with: "+ str(self.writer.get_extra_info('peername'))))
        self.signals.connectionButton.emit("Disconnect")
        self.signals.clientConnected.emit()
        executor = ThreadPoolExecutor(max_workers=2)
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
                        self.reader_task = asyncio.create_task(receive4())
                        data = await self.reader_task
                        rx_len = struct.unpack("<L",data)[0]
                        rx_len -= 4
                        rx_state = DATA

                    elif(rx_state == DATA):
                        data = await reader.readexactly(rx_len)
                        executor.submit(self.parse ,data)
                        rx_state = HEADER                            
                except asyncio.IncompleteReadError:
                    rx_state = HEADER
                except asyncio.CancelledError:
                    pass
        except ConnectionResetError:
            executor.shutdown()
            self.reader_task.cancel()
            self.signals.connectionInfo.emit("Connection terminated")
            self.signals.connectionButton.emit("Connect")
            self.signals.connectionTerminated.emit()
            return
        executor.shutdown()
        self.writer.close()
        await self.writer.wait_closed()
        self.signals.connectionInfo.emit("Connection terminated")
        self.signals.connectionButton.emit("Connect")

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


