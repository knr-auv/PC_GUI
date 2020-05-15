from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import time
from random import *
from math import *

#on windows changin pyqtgraph/ptimes.py systime.clock() to systime.process_time() is necesary
class _plot(pg.PlotWidget):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setBackground("w")
        self.setAntialiasing(True)
        self.time = [] 
        self.roll_data = []
        self.pitch_data = []
        self.yaw_data = []
        self.depth_data =[]
        roll_pen = pg.mkPen(color = (255,0,0), width = 2)
        pitch_pen = pg.mkPen(color=(0, 255, 0), width =2)
        yaw_pen = pg.mkPen(color = (0,0,255), width = 2)
        depth_pen = pg.mkPen(color = (0,0,0), width = 2)
        self.showGrid(y = True)
        self.addLegend(size =(100,30), offset =(30,30))
        #need to change later
        self.setLimits(xMin=0,  
             minXRange=10, maxXRange=100, 
             yMin=-180, yMax=180,
             minYRange=20, maxYRange=360)
        #disabling moving plot with mouse
        self.setMouseEnabled(x = False, y = False)
        #self.setMenuEnabled(enableMenu = False)
        #hiding auto button
        self.hideButtons()
        self.addLine(y=0)
        self.setDownsampling(mode = "peak")
        self.enableAutoRange()
        self.roll_plot =  self.plot(self.time, self.roll_data, pen=roll_pen, name = "roll")
        self.pitch_plot = self.plot(self.time, self.pitch_data, pen = pitch_pen, name = "pitch")
        self.yaw_plot = self.plot(self.time, self.yaw_data, pen = yaw_pen, name = "yaw")
        self.depth_plot = self.plot(self.time, self.depth_data, pen = depth_pen, name = "depth")

class IMUGraph(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(IMUGraph, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout()
        pg.setConfigOption("useOpenGL", True)
        pg.setConfigOptions(antialias=True)
        self.plot = _plot()
        layout.addWidget(self.plot)
        self.setLayout(layout)
        self.start_time = time.time()

    def update(self, arg):
        if len(self.plot.time) > 500:
            times = time.time()-self.start_time
            self.plot.time = self.plot.time[1:]
            self.plot.roll_data = self.plot.roll_data[1:]
            self.plot.pitch_data = self.plot.pitch_data[1:]
            self.plot.yaw_data = self.plot.yaw_data[1:]
            self.plot.depth_data = self.plot.depth_data[1:]
            self.plot.time.append(time.time()-self.start_time)
            self.plot.roll_data.append(arg[0])
            self.plot.pitch_data.append(arg[1])
            self.plot.yaw_data.append(arg[2])
            self.plot.depth_data.append(arg[3])
        else:
            times = time.time()-self.start_time
            self.plot.time.append(times)
            self.plot.roll_data.append(arg[0])
            self.plot.pitch_data.append(arg[1])
            self.plot.yaw_data.append(arg[2])
            self.plot.depth_data.append(arg[3])
        #enabling auto range is a dirty solution...
        self.plot.enableAutoRange()
        self.plot.roll_plot.setData(self.plot.time, self.plot.roll_data)
        self.plot.pitch_plot.setData(self.plot.time, self.plot.pitch_data)
        self.plot.yaw_plot.setData(self.plot.time, self.plot.yaw_data)
        self.plot.depth_plot.setData(self.plot.time,self.plot.depth_data)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = accGraph()
    main.show()
    sys.exit(app.exec_())




if __name__ == '__main__':
    main()