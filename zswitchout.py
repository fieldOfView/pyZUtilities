#!/usr/bin/python3

import argparse
from zocp import ZOCP
import socket
import logging

class SwitchOutNode(ZOCP):
    # Constructor
    def __init__(self, type, ports, nodename):
        super(SwitchOutNode, self).__init__(nodename)

        self.ports = ports
        self.type = type
        self.index = 0
        self.input = None
        self.output = {}

        self.register_int('Index', self.index, 'rws', 0, self.ports-1)

        input_name = 'Input'
        if self.type == 'boolean':
            self.input = False
            self.register_bool(input_name, self.input, 'rws')
        elif self.type == 'int':
            self.input = 0
            self.register_int(input_name, self.input, 'rws')
        elif self.type == 'float':
            self.input = 0.0
            self.register_float(input_name, self.input, 'rws')
        elif self.type == 'vec2f':
            self.input = [0.0, 0.0]
            self.register_vec2f(input_name, self.input, 'rws')
        elif self.type == 'vec3f':
            self.input = [0.0, 0.0, 0.0]
            self.register_vec3f(input_name, self.input, 'rws')
        elif self.type == 'vec4f':
            self.input = [0.0, 0.0, 0.0, 0.0]
            self.register_vec4f(input_name, self.input, 'rws')
        elif self.type == 'string':
            self.input = ''
            self.register_string(input_name, self.input, 'rws')

        for port in range(0, self.ports):
            output_name = "Output %s" % port

            if self.type == 'boolean':
                self.output[output_name] = False
                self.register_bool(output_name, self.output[output_name], 're')
            elif self.type == 'int':
                self.output[output_name] = 0
                self.register_int(output_name, self.output[output_name], 're')
            elif self.type == 'float':
                self.output[output_name] = 0.0
                self.register_float(output_name, self.output[output_name], 're')
            elif self.type == 'vec2f':
                self.output[output_name] = [0.0, 0.0]
                self.register_vec2f(output_name, self.output[output_name], 're')
            elif self.type == 'vec3f':
                self.output[output_name] = [0.0, 0.0, 0.0]
                self.register_vec3f(output_name, self.output[output_name], 're')
            elif self.type == 'vec4f':
                self.output[output_name] = [0.0, 0.0, 0.0, 0.0]
                self.register_vec4f(output_name, self.output[output_name], 're')
            elif self.type == 'string':
                self.output[output_name] = ''
                self.register_string(output_name, self.output[output_name], 're')

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

        emit_output = False
        if key == "Index":
            if new_value != self.index:
                self.index = max(min(int(new_value), self.ports-1), 0)
                emit_output = True
        elif key == "Input":
            if new_value != self.input:
                self.input = new_value
                emit_output = True

        if emit_output:
            output_name = "Output %s" % self.index
            self.output[output_name] = self.input
            self.emit_signal(output_name, self.input)


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
                   help='the number of output-ports to add')
    args = parser.parse_args()

    zl = logging.getLogger("zocp")
    zl.setLevel(logging.DEBUG)

    z = SwitchOutNode(args.type, args.ports, "switch-out@%s" % socket.gethostname())
    del z
