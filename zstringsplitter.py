#!/usr/bin/python3

import argparse
from zocp import ZOCP
import socket
import logging

class StringSplitterNode(ZOCP):
    # Constructor
    def __init__(self, nodename):
        super(StringSplitterNode, self).__init__()

        self.input = "" 
        self.output = ""
        self.delimiter = ','
        self.items = []
        self.index = 0

        self.set_name(nodename)
        self.register_int("Index", self.index, 'rws', min=0)
        self.register_string("Input", self.input, 'rws')
        self.register_string("Output", self.output, 're')
        self.register_string("Delimiter", self.delimiter, 'rws')

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

        item_update = False;
        if key == "Input":
            if new_value != self.input:
                self.input = new_value
                item_update = True
        elif key == "Delimiter":
            if new_value != self.delimiter:
                self.delimiter = new_value
                item_update = True
        elif key == "Index":
            if new_value != self.index:
                self.index = new_value
        else:
            return

        if item_update:
            self.items = self.input.split(self.delimiter)

        new_output = self.items[max(min(self.index,len(self.items)-1), 0)]
        if new_output != self.output:
            self.output = new_output
            self.emit_signal("Output", self.output)


if __name__ == '__main__':
    zl = logging.getLogger("zocp")
    zl.setLevel(logging.DEBUG)

    z = StringSplitterNode("stringsplitter@%s" % socket.gethostname())
    del z
