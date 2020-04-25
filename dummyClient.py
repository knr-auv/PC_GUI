import asyncio, socket, threading, struct, sys, random, time



""

class client(threading.Thread):
    HEADER = 1
    DATA = 0
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self.host = addr[0]
        self.port = addr[1]
        self.active = True
        self.rx_state = 3
        self.rx_buff_ready = True
        self.rx_buff = []
        self.tx_ready = True
        self.tx_buff = []

    async def client_handler(self):
        print('client started')
        try:
            reader, writer = await asyncio.open_connection(host = self.host, port = self.port, family = socket.AF_INET, flags = socket.SOCK_STREAM)
        except ConnectionRefusedError:
            print("connection refused")
        self.active = True
        try:
            while self.active:
                
                if len(self.tx_buff)!=0 and self.tx_ready==True:
                    writer.write(self.tx_buff.pop(0))
                    await writer.drain()
                    await asyncio.sleep(0.01)
                if(self.rx_state == self.HEADER):
                    data = await reader.read(4)
                    print("1")
                    rx_len = struct.unpack("<L",data)
                    self.rx_state = self.DATA
                elif (self.rx_state == self.DATA):
                    try:
                        data = await reader.readexactly(rx_len[0])
                        self.rx_state = self.HEADER
                        self_rx_buff_ready = False
                        self.rx_buff.append(data)
                        self_rx_buff_ready = True
                        print("here")
                    except asyncio.IncompleteReadError:
                        self.connectionInfo.emit("Message was corrupted")
                        self.rx_state = self.HEADER
            print("loop;")
        except ConnectionResetError:
            #some smart stuff TODO if the server crashes
            print("mayday")
            return
        print("wtf")
        writer.close()
        await writer.wait_closed()
        

    def run(self):
        client_thread = threading.Thread(target = lambda: asyncio.run(self.client_handler(),debug = True))
        client_thread.start()
        while self.active:
            if len(self.rx_buff)!=0 and self.rx_buff_ready:
                print(self.tx_buff.pop(0))
            data = [random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100),random.randint(0,100)]
            data = [len(struct.pack("<5I", *(data)))+4]+data
            message = struct.pack('<L5I',*(data))
            self.send(message)
            time.sleep(1)
            
        client_thread.join()
             
    def send(self, data):
        #protecting buffer
        
        self.tx_ready = False
        self.tx_buff.append(data)
        self.tx_ready = True
        #print(self.tx_buff)

    #this metod is called from client. it should pass data to parser

if __name__ == "__main__":
    thread = client(("localhost",8080))
    thread.start()
    while thread.active:
        print("act")
        time.sleep(1)
    print("thred terminated")
