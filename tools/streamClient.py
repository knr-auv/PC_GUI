import cv2
import numpy as np
import asyncio,socket, struct, logging, time
from PyQt5 import QtCore

class streamClientSignals(QtCore.QObject):
    newFrame = QtCore.pyqtSignal(object)

class StreamClient(QtCore.QThread):
    """Class creating a stream client"""

    def __init__(self, ip='10.42.0.74', port=8485):
        super(StreamClient, self).__init__()
        """Socket initialization"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        self.frame = None

    def run(self):
        self.socket.connect((self.ip, self.port))
        while True:
            try:
                self.frame = self.recive_frame()
            except:
                pass

    def stop(self):
        self.socket.close()

    def __del__(self):
        self.socket.close()

    """Method return cv2 frame from socket """
    def recive_frame(self):
        while len(self.data) < self.payload_size:
            logging.debug(str("Recv: {} port:{}".format(len(self.data), self.port)))
            self.data += self.socket.recv(4096)
        logging.debug(str("Done Recv: {}".format(len(self.data))))
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        logging.debug("msg_size: {}".format(msg_size))
        while len(self.data) < msg_size:
            self.data += self.socket.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)


class SimulationClient(QtCore.QRunnable):
    """Klasa Tworzy clienta do odbierania ramek zdjec z symulacji"""
    def __init__(self, port=44209, ip='localhost'):
        super(SimulationClient, self).__init__()
        self.signals = streamClientSignals()
        """Inicjalizacja socekta """
        self.port = port
        self.ip = ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = True
        logging.debug("Socket connect port:{}".format(port))
        self.data = b""
        self.frame = None
        
    def run(self):
        self.socket.connect((self.ip, self.port))
        while self.active:
            self.signals.newFrame.emit(self.receive_frame())
            #around 60 fps
            time.sleep(0.016)
            
    def stop(self):
        self.socket.close()

    def __del__(self):
        self.socket.close()

    """Metdoa zwraca klatke OpenCV uzyskana z Symulacji"""
    def receive_frame(self):
        self.data = b""
        self.socket.send(b"\x69")
        confirm = self.socket.recv(1)
        if not(confirm == b"\x69"):
            logging.debug("Message error")
        lenght = self.socket.recv(4)
        lenght = struct.unpack('<I', lenght)[0]
        while not(len(self.data) >= lenght):
            self.data += self.socket.recv(4096)
        return self.data