#!/usr/bin/python3

import argparse
from zocp import ZOCP
import socket
import logging

class SwitchInNode(ZOCP):
    # Constructor
    def __init__(self, type, ports, nodename = ""):
        self.nodename = nodename
        self.ports = ports
        self.type = type
        self.switch = 1
        self.input = {}
        self.output = None
        super(SwitchInNode, self).__init__()


    def run(self):
        self.set_name(self.nodename)
        self.register_int('Switch', self.switch, 'rws', 1, self.ports)

        output_name = 'Output'
        if self.type == 'boolean':
            self.output = False
            self.register_bool(output_name, self.output, 'rwe')
        elif self.type == 'int':
            self.output = 0
            self.register_int(output_name, self.output, 'rwe')
        elif self.type == 'float':
            self.output = 0.0
            self.register_bool(output_name, self.output, 'rwe')
        elif self.type == 'vec2f':
            self.output = [0.0, 0.0]
            self.register_bool(output_name, self.output, 'rwe')
        elif self.type == 'vec3f':
            self.output = [0.0, 0.0, 0.0]
            self.register_bool(output_name, self.output, 'rwe')
        elif self.type == 'vec4f':
            self.output = [0.0, 0.0, 0.0, 0.0]
            self.register_bool(output_name, self.output, 'rwe')
        elif self.type == 'string':
            self.output = ''
            self.register_bool(output_name, self.output, 'rwe')

        for port in range(1, self.ports + 1):
            input_name = "Input %s" % port

            if self.type == 'boolean':
                self.input[input_name] = False
                self.register_bool(input_name, self.input[input_name], 'rws')
            elif self.type == 'int':
                self.input[input_name] = 0
                self.register_int(input_name, self.input[input_name], 'rws')
            elif self.type == 'float':
                self.input[input_name] = 0.0
                self.register_bool(input_name, self.input[input_name], 'rws')
            elif self.type == 'vec2f':
                self.input[input_name] = [0.0, 0.0]
                self.register_bool(input_name, self.input[input_name], 'rws')
            elif self.type == 'vec3f':
                self.input[input_name] = [0.0, 0.0, 0.0]
                self.register_bool(input_name, self.input[input_name], 'rws')
            elif self.type == 'vec4f':
                self.input[input_name] = [0.0, 0.0, 0.0, 0.0]
                self.register_bool(input_name, self.input[input_name], 'rws')
            elif self.type == 'string':
                self.input[input_name] = ''
                self.register_bool(input_name, self.input[input_name], 'rws')

        self.start()
        super(SwitchInNode, self).run()

    
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

        print(key, new_value)
        if key == "Switch":
            if new_value != self.switch:
                self.switch = int(new_value)
                input_name = "Input %s" % self.switch
                self.emit_signal("Output", self.input[input_name])
        elif key.startswith("Input"):
            if new_value != self.input[key]:
                self.input[key] = new_value
                if self.switch == int(key[5:]):
                    self.output = new_value
                    self.emit_signal("Output", new_value)


def int_gt1(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("int_gt1 must be greater than 1: '%s'" % value)
    return ivalue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('type', nargs='?', choices=['boolean', 'int', 'float', 'vec2f', 'vec3f', 'vec4f', 'string'],
                   help='the type of ports to use for input and output')
    parser.add_argument('ports', metavar='N', nargs='?', type=int_gt1, default=2,
                   help='the number of input-ports to add')
    args = parser.parse_args()

    zl = logging.getLogger("zocp")
    zl.setLevel(logging.DEBUG)

    z = SwitchInNode(args.type, args.ports, "switch-in@%s" % socket.gethostname())
    z.run()
    del z
