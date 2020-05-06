import asyncio,socket, struct,  random
from concurrent.futures import ThreadPoolExecutor

class sender():
    def send(self):
        pass
    def send_msg(self, msg):
        header = struct.pack('<i', len(msg)+ 4)
        msg = bytearray(header+msg)
        self.send(msg)
        
    PID = 0
    MOTORS = 1
    BOAT_DATA = 2

    def sendPid(self, PID = []):
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
            print(axis+"is not a valid argument of pidSend. Valid arguments: 'roll', 'pitch', 'yaw', 'all'")
            return
        PID.pop(0)
        if spec != 4:
            tx_buffer = [self.PID,spec]  + PID
            tx_buffer = struct.pack('<2B3f', *(tx_buffer))
            self.send_msg(tx_buffer)
        elif spec == 4:
            tx_buffer = [self.PID,spec]  + PID
            tx_buffer = struct.pack('<2B9f', *(tx_buffer))
            self.send_msg(tx_buffer)
            
    def sendMotors(self,data): 
        
        tx_buffer = [self.MOTORS]+data
        tx_buffer = struct.pack('<B5f', *(tx_buffer))
        self.send_msg(tx_buffer)
        
    def sendBoatData(self, data =[]):
        tx_buffer = [self.BOAT_DATA]+data
        tx_buffer = struct.pack('<B5f', *(tx_buffer))
        self.send_msg(tx_buffer)

class parser():
    
    PID_RECEIVED = 0
    PID_REQUEST = 1
    
    def parser(self, data):
        if data[0] == self.PID_RECEIVED:
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
                self.setPIDs(msg)
            elif data[1]==ALL:
                msg  = struct.unpack('<2B9f', data)
                msg = list(msg)
                msg.pop(0)
                msg[0]='all'
                self.setPIDs(msg)
                
        if data[0] == self.PID_REQUEST:
            msg = struct.unpack('<2B',data)
            if msg[1]==ROLL:
                msg[1] = 'roll'
            elif msg[1]==PITCH:
                msg[1] ='pitch'
            elif msg[1]==YAW:
                 msg[1]='yaw'
            elif msg[1]== ALL:
                msg[1] = 'all'
            self.sendPID(self.getPID(msg[1]))
            
class connectionHandler(sender,parser):
     
    def __init__(self, addr, getPID, getMotors):
        super(connectionHandler, self).__init__()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.methodCollector(getPID, getMotors)
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
        self.tx_ready = True
        self.tx_buff = []
        self.clientConnected = False
        self.sendingActive = False

    def methodCollector(self, getPID, getMotors): #getDepth, getHummidity...
        self.getPID = getPID
        self.getMotors = getMotors
        

    def start_sending(self, interval = 0.03):
        self.interval = interval
        self.executor.submit(lambda: asyncio.run(self.loop()))
        
    def stop_sending(self):
        self.sendingActive = False
    def start_serving(self):
        self.executor.submit(self.run)

    async def loop(self):
        if self.clientConnected:
            self.sendingActive = True
            
            while self.clientConnected and self.sendingActive:
                await asyncio.sleep(self.interval)
                
                self.sendMotors(self.getMotors())
                
            self.sendingActive = False

    async def clientHandler(self, reader,writer):
        HEADER = 0
        DATA = 1
        rx_state = HEADER
        print("client connected")
        self.writer = writer
        self.client_loop = asyncio.get_running_loop()
        self.clientConnected = True
        
        try:
            while self.active:    
                
                if(rx_state ==HEADER):
                    async def receive4():
                        data = await reader.read(4)
                        return data
                    self.reader_task = asyncio.create_task(receive4())
                    data = await self.reader_task
                    if data == b'':
                        raise ConnectionResetError
                            
                    rx_len = struct.unpack("<L",data)[0]
                    rx_len -= 4
                    rx_state = DATA

                elif(rx_state == DATA):
                    data = await reader.readexactly(rx_len)
                    self.executor.submit(self.parse ,data)
                    rx_state = HEADER
        except asyncio.IncompleteReadError as er:
                print(er)
                rx_state = HEADER
        except asyncio.CancelledError:
                
                pass
        except ConnectionResetError:
            self.clientConnected = False
            print("Client disconnected")
            return
        print("closing")
        self.clientConnected = False
        writer.close()
        await writer.wait_closed()
        return


    async def serverHandler(self):
        self.server = await asyncio.start_server(self.clientHandler, self.host, self.port, family = socket.AF_INET, flags = socket.SOCK_STREAM)
        print("Server is listening: " + str(self.host)+":"+str(self.port))
        try:
           async with self.server:
                await self.server.serve_forever()
       
        except asyncio.CancelledError:
            self.active=False
            print("Server terminated")
            await self.server.wait_closed()
    
    def run(self):
        asyncio.run(self.serverHandler(),debug =True)

    
    def stop(self):
        async def coro():
            self.active= False
            await self.server.close()
        asyncio.run_coroutine_threadsafe(coro() , self.client_loop)
        
    
    def send(self, data):
        async def write():
            self.writer.write(data)
            await self.writer.drain()       
        asyncio.run_coroutine_threadsafe(write(), self.client_loop)

def dummyDataProvider(len=None, spec = None):
    data = []
    if spec ==None:
        for i in range(len):
            data.append(random.randint(0,100))
    elif spec!='all':
        for i in range(3):
            data.append(random.randint(0,10))
    elif spec=='all':
        for i in range(9):
            data.append(random.randint(0,10))
    return data

if __name__=="__main__":
    addr = ("localhost", 8080)
    server = connectionHandler(addr, lambda arg: dummyDataProvider(spec = arg), lambda: dummyDataProvider(len=5))
    server.start_serving()

   
