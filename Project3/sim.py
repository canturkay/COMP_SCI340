import sys
import logging

from simulator.config import *
from simulator.topology import Topology, Get_Time
from simulator.event_queue import Event_Queue


class Sim(Topology):

    def __init__(self, algorithm, event_file, step='NORMAL'):
        super().__init__(algorithm, step)
        self.load_command_file(event_file)
        self.dump_sim()
        self.dispatch_event(self.step)
        self.logging.info("Total messages sent: %d" % self.message_count)

    def __str__(self):
        ans = "==== Print Topology ====\n"
        ans += super().__str__()
        ans += "==== Print Event ====\n"
        ans += Event_Queue.Str()
        return ans

    def dump_sim(self):
        self.logging.info("DUMP_SIM at Time %d\n" % Get_Time() + str(self))

    def dispatch_event(self, step='NORMAL'):
        e = Event_Queue.Get_Earliest()
        while e:
            e.dispatch()
            if step == 'SINGLE_STEP':
                self.logging.info(str(e))
                self.wait()
            e = Event_Queue.Get_Earliest()

    def print_comment(self, comment):
        self.logging.info('Time: %d, Comment: %s' % (Get_Time(), comment))


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4 or sys.argv[1] not in ROUTE_ALGORITHM:
        sys.stderr.write(USAGE_STR)
        sys.exit(-1)

    step = 'NO_STOP'
    if len(sys.argv) == 4:
        if sys.argv[3] not in STEP_COMMAND:
            sys.stderr.write(USAGE_STR)
            sys.exit(-1)
        else:
            step = sys.argv[3]

    s = Sim(sys.argv[1], sys.argv[2], step)


if __name__ == '__main__':
    # Try: python sim.py GENERIC demo.event
    # Change logging level from DEBUG to INFO or WARNING, if DEBUG information bothers you
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, datefmt=LOGGING_DATAFMT)
    main()
