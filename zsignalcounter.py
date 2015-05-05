#!/usr/bin/python3

from zocp import ZOCP
import socket
import logging
import time

class CounterNode(ZOCP):
    # Constructor
    def __init__(self, nodename=""):
        self.nodename = nodename
        self.input = ""
        self.count = 0
        self.count_period = 0
        self.sps = 0
        self.interval = 1.0
        self.loop_time = 0
        super(CounterNode, self).__init__()


    def run(self):
        self.set_name(self.nodename)
        self.register_string("Input", "", 's')
        self.register_int("Count", 0, 'r')
        self.register_int("Signals per second", 0, 'r')
        self.start()

        while True:
            try:
                self.run_once(0)
                if time.time() > self.loop_time:
                    self.loop_time = time.time() + self.interval
                    self.on_timer()
            except (KeyboardInterrupt, SystemExit):
                break

    
    def on_peer_signaled(self, peer, name, data, *args, **kwargs):
        self.count = self.count + 1;
        self.count_period = self.count_period + 1;
        self.emit_signal("Count", self.count)


    def on_timer(self):
        mix = 0.9
        self.sps = self.sps * (1-mix) + self.count_period * mix
        self.sps = round(self.sps*100)/100
        self.count_period = 0
        self.emit_signal("Signals per second", self.sps)


if __name__ == '__main__':
    zl = logging.getLogger("zocp")
    zl.setLevel(logging.INFO)

    z = CounterNode("signalcounter@%s" % socket.gethostname())
    z.run()
    z.stop()
    z = None
    print("FINISH")
