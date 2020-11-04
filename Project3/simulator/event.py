import sys

from simulator.config import *


class Event:

    def __init__(self, time_stamp, event_type, sim, arg1 = -1, arg2 = -1, arg3 = -1):
        self.time_stamp = time_stamp
        self.event_type = event_type
        self.sim = sim

        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3

    def __lt__(self, other):
        if self.time_stamp == other.time_stamp:
            if self.event_type != EVENT_TYPE.SEND_LINK and other.event_type == EVENT_TYPE.SEND_LINK:
                return True
        return self.time_stamp < other.time_stamp

    def __str__(self):
        args = ""
        if self.arg1 != -1:
            args += " " + str(self.arg1)
        if self.arg2 != -1:
            args += " " + str(self.arg2)
        if self.arg3 != -1:
            args += " " + str(self.arg3)

        return "Time_Stamp: " + str(self.time_stamp) + " Event_Type: " + self.event_type + args

    def dispatch(self):
        if self.event_type == EVENT_TYPE.ADD_NODE:
            self.sim.add_node(self.arg1)
        elif self.event_type == EVENT_TYPE.ADD_LINK:
            self.sim.add_link(self.arg1, self.arg2, self.arg3)
        elif self.event_type == EVENT_TYPE.CHANGE_LINK:
            self.sim.change_link(self.arg1, self.arg2, self. arg3)
        elif self.event_type == EVENT_TYPE.DELETE_LINK:
            self.sim.delete_link(self.arg1, self.arg2)
        elif self.event_type == EVENT_TYPE.DELETE_NODE:
            self.sim.delete_node(self.arg1)
        elif self.event_type == EVENT_TYPE.PRINT:
            self.sim.print_comment(self.arg1)
        elif self.event_type == EVENT_TYPE.DUMP_NODE:
            self.sim.dump_node(self.arg1)
        elif self.event_type == EVENT_TYPE.DRAW_TOPOLOGY:
            self.sim.draw_topology()
        elif self.event_type == EVENT_TYPE.ROUTING_MESSAGE_ARRIVAL:
            self.sim.routing_message_arrival(self.arg1, self.arg2)
        elif self.event_type == EVENT_TYPE.DUMP_SIM:
            self.sim.dump_sim()
        elif self.event_type == EVENT_TYPE.DRAW_PATH:
            self.sim.draw_path(self.arg1, self.arg2)
        elif self.event_type == EVENT_TYPE.DRAW_TREE:
            self.sim.draw_tree(self.arg1)
        elif self.event_type == EVENT_TYPE.SEND_LINK:
            self.sim.send_link(self.arg1, self.arg2, self.arg3)
        else:
            pass
            # sys.stderr.write("Unknown event type %s" % self.event_type)
            # sys.exit(-1)
