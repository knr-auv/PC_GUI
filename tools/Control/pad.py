from PyQt5 import QtCore
import inputs, json, time, math, logging, threading


class padSteering(QtCore.QRunnable):
    def __init__(self, config = None):
        #TODO selecting pad...
        super(PadSteering, self).__init__()
        self.getData_callback = None
        self.mode = "pad"
        with open("tools/pad.json",'r') as fd:
            self.input = json.load(fd)
        self.active = True
        self.config=config
        self.lock = threading.Lock()
        self.gamepad = inputs.devices.gamepads[0]
        self.output = {"vertical": 0, 'roll':0, 'pitch':0, "yaw":0, "throttle":0}
    def checkDevice():
        if len(inputs.devices.gamepads):
            return True
        return False

    def process_input(self, event):
        #event types that i dont care
        if event.ev_type == 'Sync':
            return
        if event.ev_type == 'Misc':
            return
        #probably good solution
        for i in self.input:
            if event.code == i:
                if event.code!= 'ABS_Z' and event.code!='ABS_RZ':
                    if abs(event.state)<self.config["pad_deadzone"]:
                        self.input[i]=0
                        return
                self.input[i]=event.state

    def catch_input(self):
        events = self.gamepad.read()
        for i in events:
            self.process_input(i)

    def expo(self, input, out_max, index):
        if(out_max==0):
            return 0
        return (pow(abs(input), index)/pow(out_max, index))

    def map(self,input,in_min,in_max,out_min,out_max):
        return (input-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
    
    def scale(self):
        self.output["vertical"] = int(self.map((self.input["ABS_RZ"]-self.input["ABS_Z"]),-255,255,-self.config['max_vertical'],self.config['max_vertical']))
        self.output["roll"] = -self.map(self.input["ABS_RX"],-32767,32767,-self.config["max_roll"],self.config["max_roll"])
        self.output["pitch"] = -self.map(self.input["ABS_RY"],-32767,32767,-self.config["max_pitch"],self.config["max_pitch"])
        self.output["yaw"] = int(self.map(self.input["ABS_X"],-32767,32767,-self.config['max_yaw'],self.config['max_yaw']))
        self.output["throttle"] = int(self.map(self.input["ABS_Y"],-32767,32767,-self.config['max_throttle'],self.config['max_throttle']))

    def calculate_expo(self):
        for i in self.output:
            self.output[i]*=self.expo(self.output[i],self.config['max_'+i], self.config[i+'_expo'])

    def get_raw(self):
        return[self.input["ABS_X"],self.input["ABS_Y"], self.input["ABS_RX"], self.input["ABS_RY"],self.input["ABS_Z"], self.input["ABS_RZ"]]

    def get_data(self):
        with self.lock:
            self.scale()    #scale needs to be before expo!!!
            self.calculate_expo()
            self.getData_callback.emit([self.output["roll"],self.output["pitch"],int(self.output["yaw"]),int(self.output["vertical"]),int(self.output["throttle"])])

    def run(self):

        while self.active:
            self.catch_input()
        self.active = True

if __name__=="__main__":
    a = PadSteering()
    while True:
        a.catch_input()
        a.scale()
        print(a.get_data())
        time.sleep(0.0001)