#!/usr/bin/python3

from zocp import ZOCP
import socket
import logging

class MultiplierNode(ZOCP):
    # Constructor
    def __init__(self, nodename=""):
        self.nodename = nodename
        self.factor = 1.0
        self.input = 0.0
        self.output = None
        self.inverse = False
        super(MultiplierNode, self).__init__()


    def run(self):
        self.set_name(self.nodename)
        self.register_float("Factor", self.factor, 'rw')
        self.register_bool("Inverse", False, 'rw')
        self.register_float("Value", self.input, 'rwes')
        self.start()

        super(MultiplierNode, self).run()

    
    def on_modified(self, peer, name, data, *args, **kwargs):
        if self._running and peer:
            for key in data:
                if 'value' in data[key]:
                    self.receive_value(key)

                
    def on_peer_signaled(self, peer, name, data, *args, **kwargs):
        if self._running and peer:
            for sensor in data[2]:
                if(sensor):
                    self.receive_value(sensor)


    def receive_value(self, key):
        new_value = self.capability[key]['value']

        if key == "Inverse":
            if new_value != self.factor:
                self.inverse = new_value
        elif key == "Factor":
            if new_value != self.factor:
                self.factor = new_value
        elif key == "Value":
            if new_value != self.input:
                self.input = new_value

        if not self.inverse:
           new_output = self.input * self.factor
        elif self.factor != 0:
           new_output = self.input / self.factor

        if new_output!=self.output:
            self.output = new_output
            self.emit_signal("Value", self.output)


if __name__ == '__main__':
    zl = logging.getLogger("zocp")
    zl.setLevel(logging.DEBUG)

    z = MultiplierNode("multiplier@%s" % socket.gethostname())
    z.run()
    del z
    print("FINISH")
