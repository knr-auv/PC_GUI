import asyncio,socket, struct, threading, random



class connectionHandler(threading.Thread):
    
  
    def __init__(self, addr):
        super(connectionHandler, self).__init__()
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
        self.tx_ready = True
        self.tx_buff = []
   
                
    async def clientHandler(self, reader,writer):
        HEADER = 0
        DATA = 1
        rx_state = HEADER
        print("client connected")
        self.writer = writer
        self.client_loop = asyncio.get_running_loop()
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
                    data = struct.unpack("<5I",data)
                    print(data)
                    rx_state = HEADER
        except asyncio.IncompleteReadError as er:
                print(er)
                rx_state = HEADER
        except asyncio.CancelledError:
                
                pass
        except ConnectionResetError:
            print("Client disconnected")
            return
        print("closing")
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
        
    
    def send(self):
        data = [random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)]
        data = [len(struct.pack("<5I", *(data)))+4]+data
        message = struct.pack('<L5I',*(data))
        async def write():
            self.writer.write(message)
            await self.writer.drain()       
        asyncio.run_coroutine_threadsafe(write(), self.client_loop)

class parser():
    def __init__(self, func):
        self.send=func

    def sendPids(P, I, D):
        tx_buffer = [0, P,I,D]
        tx_buffer = struct.pack('<2i3f', *([4+len(tx_buffer)]+tx_buffer))
        self.send(tx_buffer)

if __name__=="__main__":
    server = connectionHandler(("localhost", 8080))
    server.start()
