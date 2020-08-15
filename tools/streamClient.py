
import numpy as np
import asyncio,socket, struct, logging, time
from PyQt5 import QtCore

class streamClientSignals(QtCore.QObject):
    newFrame = QtCore.pyqtSignal(object)
    connectionReset = QtCore.pyqtSignal()


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
        self.socket.connect(('localhost', 8090))
        while self.active:
            self.signals.newFrame.emit(self.receive_frame())
            #around 40 fps
            
            time.sleep(0.035)
            
    def stop(self):
        self.socket.close()

    def __del__(self):
        self.socket.close()

    """Metdoa zwraca klatke OpenCV uzyskana z Symulacji"""
    def receive_frame(self):
        try:
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
        except:
            pass