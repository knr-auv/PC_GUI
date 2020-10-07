
import numpy as np
import asyncio,socket, struct, logging, time, pickle
from PyQt5 import QtCore

class streamClientSignals(QtCore.QObject):
    connectionReset = QtCore.pyqtSignal()
    newDetection = QtCore.pyqtSignal(object)


class autonomyStream(QtCore.QRunnable):
    """Klasa Tworzy clienta do odbierania ramek zdjec z symulacji"""
    def __init__(self, port=6969, ip='localhost'):
        super(autonomyStream, self).__init__()
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
        self.socket.connect(('localhost', self.port))
        try:
            while self.active:
                a =self.socket.recv(1)
                if a == b"\x68":  
                    self.signals.newDetection.emit(self.receive_detection())
        except ConnectionAbortedError:
            pass

    def stop(self):
        self.active = False
        self.socket.close()

    def __del__(self):
        self.socket.close()

    def receive_detection(self):
        try:
            data = b""
            self.socket.send(b"\x68")
            lenght = self.socket.recv(4)
            lenght = struct.unpack('<I', lenght)[0]
            while not(len(data) >= lenght):
                data += self.socket.recv(4096)

            return pickle.loads(data)
        except:
            print("error")
            return -1