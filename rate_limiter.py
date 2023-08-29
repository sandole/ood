from time import time, sleep


class SlidingWindow:

    def __init__(self, capacity, time_unit, forward_callback, drop_callback):
        self.capacity = capacity
        self.time_unit = time_unit
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback

        self.cur_time = time()
        self.pre_count = capacity
        self.cur_count = 0
        
    def handle(self, packet): #1
        if (time() - self.cur_time) > self.time_unit: #2
            self.cur_time = time()
            self.pre_count = self.cur_count
            self.cur_count = 0

        ec = (self.pre_count * (self.time_unit - (time() - self.cur_time)) / self.time_unit) + self.cur_count #3

        if (ec > self.capacity): #4
            return self.drop_callback(packet)

        self.cur_count += 1 #5
        return self.forward_callback(packet)
    
def forward(packet):
    print("Packet Forwarded: " + str(packet))


def drop(packet):
    print("Packet Dropped: " + str(packet))


throttle = SlidingWindow(5, 1, forward, drop)

packet = 0

while True:
    sleep(0.1)
    throttle.handle(packet)
    packet += 1
