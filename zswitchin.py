#!/usr/bin/python3

import argparse
from zocp import ZOCP
import socket
import logging

class SwitchInNode(ZOCP):
    # Constructor
    def __init__(self, type, ports, nodename):
        super(SwitchInNode, self).__init__(nodename)
        self.ports = ports
        self.type = type
        self.index = 0
        self.input = {}
        self.output = None

        self.register_int('Index', self.index, 'rws', 0, self.ports-1)

        output_name = 'Output'
        if self.type == 'boolean':
            self.output = False
            self.register_bool(output_name, self.output, 're')
        elif self.type == 'int':
            self.output = 0
            self.register_int(output_name, self.output, 're')
        elif self.type == 'float':
            self.output = 0.0
            self.register_float(output_name, self.output, 're')
        elif self.type == 'vec2f':
            self.output = [0.0, 0.0]
            self.register_vec2f(output_name, self.output, 're')
        elif self.type == 'vec3f':
            self.output = [0.0, 0.0, 0.0]
            self.register_vec3f(output_name, self.output, 're')
        elif self.type == 'vec4f':
            self.output = [0.0, 0.0, 0.0, 0.0]
            self.register_vec4f(output_name, self.output, 're')
        elif self.type == 'string':
            self.output = ''
            self.register_string(output_name, self.output, 're')

        for port in range(0, self.ports):
            input_name = "Input %s" % port

            if self.type == 'boolean':
                self.input[input_name] = False
                self.register_bool(input_name, self.input[input_name], 'rws')
            elif self.type == 'int':
                self.input[input_name] = 0
                self.register_int(input_name, self.input[input_name], 'rws')
            elif self.type == 'float':
                self.input[input_name] = 0.0
                self.register_float(input_name, self.input[input_name], 'rws')
            elif self.type == 'vec2f':
                self.input[input_name] = [0.0, 0.0]
                self.register_vec2f(input_name, self.input[input_name], 'rws')
            elif self.type == 'vec3f':
                self.input[input_name] = [0.0, 0.0, 0.0]
                self.register_vec3f(input_name, self.input[input_name], 'rws')
            elif self.type == 'vec4f':
                self.input[input_name] = [0.0, 0.0, 0.0, 0.0]
                self.register_vec4f(input_name, self.input[input_name], 'rws')
            elif self.type == 'string':
                self.input[input_name] = ''
                self.register_string(input_name, self.input[input_name], 'rws')

        self.start()
        self.run()

    
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

        if key == "Index":
            if new_value != self.index:
                self.index = max(min(int(new_value), self.ports-1), 0)
                input_name = "Input %s" % self.index
                self.emit_signal("Output", self.input[input_name])
        elif key.startswith("Input"):
            if new_value != self.input[key]:
                self.input[key] = new_value
                if self.index == int(key[5:]):
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
    del z
