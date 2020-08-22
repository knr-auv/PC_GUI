import asyncio,socket, struct, threading, logging

from PyQt5 import QtCore
from concurrent.futures import ThreadPoolExecutor

class odroidClientSignals(QtCore.QObject):
    armed = QtCore.pyqtSignal()
    disarmed = QtCore.pyqtSignal()
    receivedPID = QtCore.pyqtSignal(object)
    receivedMotors = QtCore.pyqtSignal(object)
    receivedBoatData = QtCore.pyqtSignal(object)
    receivedIMUData = QtCore.pyqtSignal(object)
    connectionInfo = QtCore.pyqtSignal(object)
    connectionButton = QtCore.pyqtSignal(object)
    connectionTerminated = QtCore.pyqtSignal()
    connectionRefused = QtCore.pyqtSignal()
    clientConnected = QtCore.pyqtSignal()
    receivedAutonomyMsg = QtCore.pyqtSignal(object)

class parser():
    def parse(self, data):
        proto = self.protocol["TO_GUI"]
        pid_spec = self.protocol["PID_SPEC"]
        control_spec = self.protocol["CONTROL_SPEC"]
        try:
            if data[0]== proto["PID"]:
                ROLL = 1
                PITCH = 2
                YAW = 3
                ALL = 4
                if data[1]!= ALL:
                    msg = struct.unpack('<2B3f', data)
                    msg = list(msg)
                    msg.pop(0)
                    if msg[0]==pid_spec["roll"]:
                        msg[0] = 'roll'
                    elif msg[0]==pid_spec["pitch"]:
                        msg[0] ='pitch'
                    elif msg[0]==pid_spec["yaw"]:
                        msg[0]='yaw'
                    self.signals.receivedPID.emit(msg)
                elif data[1]==pid_spec["all"]:
                    msg  = struct.unpack('<2B9f', data)
                    msg = list(msg)
                    msg.pop(0)
                    msg[0]='all'
                    self.signals.receivedPID.emit(msg)

            elif data[0]==proto["MOTORS"]:
                msg = struct.unpack('<B5f', data)
                msg = list(msg)
                msg.pop(0)
                self.signals.receivedMotors.emit(msg)

            elif data[0] == proto["BOAT_DATA"]:
                msg = struct.unpack('<2B'+str(data[1])+'s',data)
                self.signals.receivedBoatData.emit(msg[2])

            elif data[0] == proto["IMU"]:
                msg = struct.unpack('<B4f',data)
                msg = list(msg)
                msg.pop(0)
                self.signals.receivedIMUData.emit(msg)

            elif data[0] == proto["CONTROL"]:
                if data[1]==control_spec["ARMED"]:
                    logging.debug("ARMED")
                    self.signals.armed.emit()
                elif data[1]==control_spec["DISARMED"]:
                    logging.debug("DISARMED")
                    self.signals.disarmed.emit()

            elif data[0] == proto["AUTONOMY_MSG"]:
                msg = struct.unpack('<2B'+str(data[1])+'s',data)
                text = msg[2].decode('utf-8')
                self.signals.receivedAutonomyMsg.emit(text)

        except:
            sys.exc_info()
            logging.critical("error while parsing data")

class sender():
    def __init__(self, protocol):
        self.proto = protocol["TO_ODROID"]
        self.pid_spec = protocol["PID_SPEC"]
        self.control_spec = protocol['CONTROL_SPEC']

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
            spec=self.pid_spec["roll"]
        elif axis =='pitch':
            spec = self.pid_spec["pitch"]
        elif axis == 'yaw':
            spec = self.pid_spec["yaw"]
        elif axis =='all':
            spec = self.pid_spec["all"]
        else:
            logging.debug(str(axis)+"is not a valid argument of sendPid. Valid arguments: 'roll', 'pitch', 'yaw', 'all'")
            return
        PID.pop(0)
        if spec != 4:
            tx_buffer = [self.proto["PID"],spec]  + PID
            tx_buffer = struct.pack('<2B3f', *(tx_buffer))
            self.send_msg(tx_buffer)
        elif spec == 4:
            tx_buffer = [self.proto["PID"],spec]  + PID
            tx_buffer = struct.pack('<2B9f', *(tx_buffer))
            self.send_msg(tx_buffer)

    def sendControl(self, msg):
        if msg[0] == self.control_spec['START_TELEMETRY']:
            tx_buffer = [self.proto["CONTROL"]]+msg
            tx_buffer = struct.pack('<2BI',*(tx_buffer))
            self.send_msg(tx_buffer)
        elif msg[0] == self.control_spec['STOP_TELEMETRY']:
            tx_buffer = [self.proto["CONTROL"]]+msg
            tx_buffer = struct.pack('<2B',*(tx_buffer))
            self.send_msg(tx_buffer)

        elif msg[0] == self.control_spec['START_PID']:
            tx_buffer = [self.proto["CONTROL"]]+msg
            tx_buffer = struct.pack('<2BI',*(tx_buffer))
            self.send_msg(tx_buffer)

        elif msg[0] == self.control_spec['STOP_PID']:
            tx_buffer = [self.proto["CONTROL"]]+msg
            tx_buffer = struct.pack('<2B',*(tx_buffer))
            self.send_msg(tx_buffer)
        elif msg[0]==self.control_spec['START_AUTONOMY']:
            tx_buffer = [self.proto["CONTROL"]]+msg
            tx_buffer = struct.pack('<2B',*(tx_buffer))
            self.send_msg(tx_buffer)
           
        elif msg[0]==self.control_spec['STOP_AUTONOMY']:
            tx_buffer = [self.proto["CONTROL"]]+msg
            tx_buffer = struct.pack('<2B',*(tx_buffer))
            self.send_msg(tx_buffer)

    def sendPIDRequest(self, axis):
        if axis=='roll':
            spec=self.pid_spec["roll"]
        elif axis =='pitch':
            spec = self.pid_spec["pitch"]
        elif axis == 'yaw':
            spec = self.pid_spec["yaw"]
        elif axis =='all':
            spec = self.pid_spec["all"]
        else:
            logging.debug(axis+"is not a valid argument of pidSend. Valid arguments: 'roll', 'pitch', 'yaw', 'all'")
            return
        tx_buffer = [self.proto["PID_REQUEST"],spec]
        tx_buffer = struct.pack('<2B',*(tx_buffer))
        self.send_msg(tx_buffer)

    def sendBoatDataRequest(self):
        tx_buffer = [self.proto["BOAT_DATA_REQUEST"]]
        tx_buffer = struct.pack('<B',*(tx_buffer))
        self.send_msg(tx_buffer)

    def sendInput(self, data):
        tx_buffer=[self.proto['PAD']]+data
        tx_buffer = struct.pack('<B2f3i',*(tx_buffer))
        self.send_msg(tx_buffer)
        if(self.checked==False):
            self.checked = True
            logging.debug("Msg was sent succesfully, connection with odroid has been established")

class odroidClient(QtCore.QRunnable, parser,sender):
    def __init__(self, addr, protocol):
        QtCore.QRunnable.__init__(self)
        sender.__init__(self,protocol)
        self.signals = odroidClientSignals()
        self.protocol = protocol
        #self.parser = parser()
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
        self.checked = False

    def start_telemetry(self, interval):
        self.sendControl([self.protocol["CONTROL_SPEC"]["START_TELEMETRY"],interval])
        logging.debug("Starting telemetry")

    def disarm(self):
        logging.debug("DISARMING")
        self.sendControl([self.protocol["CONTROL_SPEC"]["STOP_PID"]])
        
    def arm(self, interval):
        logging.debug("ARMING")
        self.sendControl([self.protocol["CONTROL_SPEC"]["START_PID"], interval])

        self.checked = False
    def startAutonomy(self):
        self.sendControl([self.protocol["CONTROL_SPEC"]["START_AUTONOMY"]])

    def stopAutonomy(self):
        self.sendControl([self.protocol["CONTROL_SPEC"]["STOP_AUTONOMY"]])

        
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
        executor = ThreadPoolExecutor(max_workers=5)
        HEADER = 0
        DATA = 1
        rx_state = HEADER
        rx_len =0
        self.start_telemetry(30)
        
        self.sendBoatDataRequest()
        self.sendPIDRequest("all")
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
        self.signals.connectionTerminated.emit()

    def run(self):
        asyncio.run(self.client(), debug = True)
        
    def stop(self):
        async def coro():
            self.reader_task.cancel() 
        self.active = False
        try:
            if self.client_loop.is_running():
                asyncio.run_coroutine_threadsafe(coro(), self.client_loop)  
        except AttributeError:
            pass


        
    def send(self, data):
        async def write():
            self.writer.write(data)
            await self.writer.drain()
        if self.client_loop.is_running():
            asyncio.run_coroutine_threadsafe(write(), self.client_loop)


