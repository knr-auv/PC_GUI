from PyQt5 import QtCore
import inputs, json, time, math, logging


class PadSteering(QtCore.QRunnable):
    def __init__(self, config = None):
        #TODO selecting pad...
        super(PadSteering, self).__init__()
        with open("tools/pad.json",'r') as fd:
            self.input = json.load(fd)
        if config == None:
            self.config={'max_roll': 45,
                         'max_pitch':45,
                         'vertical_sensivity':0.5,
                         'vertical_expo':0,
                         'roll_sensivity':0.5,
                         'pitch_sensivity':0.5,
                         'yaw_sensivity':0.5,
                         'throttle_sensivity':0}
        
        self.gamepad = inputs.devices.gamepads[0]
        self.output = {"vertical": 0, 'roll_offset':0, 'pitch_offset':0, "yaw":0, "throttle":0}
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
                    if abs(event.state)<2000:
                        self.input[i]=0
                        return
                self.input[i]=event.state

    def catch_input(self):
        events = self.gamepad.read()
        for i in events:
            self.process_input(i)
    def scale(self):
        def map(input,in_min,in_max,out_min,out_max):
            return (input-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
        self.output["vertical"] = -int(map((self.input["ABS_RZ"]-self.input["ABS_Z"]),-255,255,-1000,1000))
        self.output["roll_offset"] = map(self.input["ABS_RX"],-32767,32767,-self.config["max_roll"],self.config["max_roll"])
        self.output["pitch_offset"] = map(self.input["ABS_RY"],-32767,32767,-self.config["max_pitch"],self.config["max_pitch"])
        self.output["yaw"] = int(map(self.input["ABS_X"],-32767,32767,-1000,1000))
        self.output["throttle"] = int(map(self.input["ABS_Y"],-32767,32767,-1000,1000))

    def get_data(self):
        self.scale()
        return [self.output["roll_offset"],self.output["pitch_offset"],self.output["yaw"],self.output["vertical"],self.output["throttle"]]
        #return [self.input['ABS_X'],self.input['ABS_Y'], self.input['ABS_RX'],self.input['ABS_RY'],self.input['ABS_Z'],self.input['ABS_RZ']]+

    def run(self):
        while True:
            self.catch_input()
            time.sleep(0.02)
if __name__=="__main__":
    a = PadSteering()
    while True:
        a.catch_input()
        a.scale()
        print(a.get_data())
        time.sleep(0.0001)