import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import socket
import cv2
import pickle
import struct
import time
import numpy as np
import logging
from cameraContainer_ui import Ui_cameraContainer


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


class SimulationClient(QtCore.QThread):
    """Klasa Tworzy clienta do odbierania ramek zdjec z symulacji"""
    def __init__(self, port=44209, ip='localhost'):
        super(SimulationClient, self).__init__()
        """Inicjalizacja socekta """
        self.port = port
        self.ip = ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("Socket connect port:{}".format(port))
        self.data = b""
        self.frame = None

    def run(self):
        self.socket.connect((self.ip, self.port))
        time.sleep(1)
        while True:
            try:
                self.frame = self.recive_frame()
            except e:
                print(e)
                pass

    def stop(self):
        self.socket.close()

    def __del__(self):
        self.socket.close()

    """Metdoa zwraca klatke OpenCV uzyskana z Symulacji"""
    def recive_frame(self):
        self.data = b""
        self.socket.send(b"\x69")
        confirm = self.socket.recv(1)
        if not(confirm == b"\x69"):
            logging.debug("Message error")
        lenght = self.socket.recv(4)
        lenght = struct.unpack('<I', lenght)[0]
        while not(len(self.data) >= lenght):
            self.data += self.socket.recv(4096)
        self.data = np.fromstring(self.data, np.uint8)
        return cv2.imdecode(self.data, cv2.IMREAD_COLOR)


class cameraContainer(QtWidgets.QWidget, Ui_cameraContainer):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.connectButton.clicked.connect(self.start_client)
        self.framelabel.setScaledContents(True)
        self.capture = None
        self.timer = QtCore.QTimer(self, interval=1)
        self.timer.timeout.connect(self.update_frame)
        self._image_counter = 0
        self.client = None

    @QtCore.pyqtSlot()
    def start_client(self):
        ip, port = self.clientData.displayText().split(":")
        if self.client is None:
            self.client = SimulationClient(ip=str(ip), port=int(port))
            self.client.start()
            self.timer.start()
            self.connectButton.setText("Disconnect")
        else:
            self.timer.stop()
            self.client.stop()
            self.connectButton.setText("Connect")

    @QtCore.pyqtSlot()
    def update_frame(self):
        self.displayImage(self.client.frame, True)

    def displayImage(self, img, window=True):
        if img is not None:
            qformat = QtGui.QImage.Format_Indexed8
            if len(img.shape)==3 :
                if img.shape[2]==4:
                    qformat = QtGui.QImage.Format_RGBA8888
                else:
                    qformat = QtGui.QImage.Format_RGB888
            outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
            outImage = outImage.rgbSwapped()
            if window:
                self.framelabel.setPixmap(QtGui.QPixmap.fromImage(outImage))


if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = cameraContainer()
    window.show()
    sys.exit(app.exec_())
