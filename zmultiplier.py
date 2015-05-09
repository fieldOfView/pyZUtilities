#!/usr/bin/python3

import argparse
from zocp import ZOCP
import socket
import logging

class MultiplierNode(ZOCP):
    # Constructor
    def __init__(self, ports, factor, inverse, nodename):
        self.nodename = nodename
        self.factor = factor
        self.ports = ports
        self.input = {}
        self.output = {}
        self.inverse = inverse
        super(MultiplierNode, self).__init__()


    def run(self):
        self.set_name(self.nodename)
        self.register_float("Factor", self.factor, 'rws')
        self.register_bool("Inverse", False, 'rw')

        for port in range(1, self.ports + 1):
            if self.ports == 1:
                input_name = "Input"
                output_name = "Output"
            else:
                input_name = "Input %s" % port
                output_name = "Output %s" % port
            self.input[input_name] = 0.
            self.output[output_name] = 0.
            self.register_float(input_name, self.input[input_name], 'rws')
            self.register_float(output_name, self.output[output_name], 're')

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
        value_key = False

        if key == "Inverse":
            if new_value != self.factor:
                self.inverse = new_value
        elif key == "Factor":
            if new_value != self.factor:
                self.factor = new_value
        elif key.startswith("Input"):
            if new_value != self.input[key]:
                self.input[key] = new_value
                self.handle_value(key)
                return
        else:
            return

        # Inverse or Factor were changed
        for input_key in self.input.keys():
            self.handle_value(input_key)


    def handle_value(self, input_key):
        output_key = "Output" + input_key[5:]
        if not self.inverse:
            new_output = self.input[input_key] * self.factor
        elif self.factor != 0:
            new_output = self.input[input_key] / self.factor

        if new_output != self.output[output_key]:
            self.output[output_key] = new_output
            self.emit_signal(output_key, new_output)




def int_gt0(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("invalid value: int must be greater than 0: '%s'" %
                                         value)
    return ivalue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ports', metavar='N', nargs='?', type=int_gt0, default=1,
                   help='the number of ports to add, all multiplied by the same factor')
    parser.add_argument('-f --factor', dest='factor', metavar='F', type=float, default=1.0,
                   help='initial value of Factor')
    parser.add_argument('-i --inverse', dest='inverse', action='store_true', default=False,
                   help='multiply (False) or divide (True) by factor')
    args = parser.parse_args()

    zl = logging.getLogger("zocp")
    zl.setLevel(logging.DEBUG)

    z = MultiplierNode(args.ports, args.factor, args.inverse,
                       "multiplier@%s" % socket.gethostname())
    z.run()
    del z
