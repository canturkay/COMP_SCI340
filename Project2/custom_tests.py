import itertools
import sys
import time

import lossy_socket
from streamer import Streamer

NUMS = 10000


def receive(s):
    expected = 0
    str_buf = ""
    while expected < NUMS:
        data = s.recv()
        print("recv returned {%s}" % data.decode('utf-8'))
        str_buf += data.decode('utf-8')
        for t in str_buf.split(" "):
            if len(t) == 0:
                # there could be a "" at the start or the end, if a space is there
                continue
            if int(t) == expected:
                # print("got %d!" % expected)
                expected += 1
                str_buf = ''
            elif int(t) > expected:
                print("ERROR: got %s but was expecting %d" % (t, expected))
                sys.exit(-1)
            else:
                # we only received the first part of the number at the end
                # we must leave it in the buffer and read more.
                str_buf = t
                break


def host1(listen_port, remote_port):
    s = Streamer(dst_ip="localhost", dst_port=remote_port,
                 src_ip="localhost", src_port=listen_port)
    receive(s)
    print("STAGE 1 TEST PASSED!")
    # send large chunks of data
    i = 0
    buf = ""
    while i < NUMS:
        buf += ("%d " % i)
        if len(buf) > 12345 or i == NUMS - 1:
            # print("sending {%s}" % buf)
            s.send(buf.encode('utf-8'))
            buf = ""
        i += 1
    s.close()
    print("CHECK THE OTHER SCRIPT FOR STAGE 2 RESULTS.")


def host2(listen_port, remote_port):
    s = Streamer(dst_ip="localhost", dst_port=remote_port,
                 src_ip="localhost", src_port=listen_port)
    # send small pieces of data
    for i in range(NUMS):
        buf = ("%d " % i)
        # print("sending {%s}" % buf)
        s.send(buf.encode('utf-8'))
    receive(s)
    s.close()
    print("STAGE 2 TEST PASSED!")


loss_rates = [0, 0.1, 0.2]
corruption_rates = [0, 0.1, 0.2]
max_delivery_delays = [0, 0.1, 0.2]

alphas = [0, 0.1, 0.2]
betas = [0, 0.1, 0.25]
default_wait_seconds = [0.0001, 0.001, 0.01]


def get_combinations(list_1: list, list_2: list) -> list:
    return list(itertools.chain([list(zip(comb, list_2)) for comb in itertools.permutations(list_1, len(list_2))]))


def main():
    combinations = get_combinations(loss_rates, corruption_rates)
                                    # get_combinations(corruption_rates,
                                    #                  get_combinations(max_delivery_delays,
                                    #                                   get_combinations(
                                    #                                       alphas,
                                    #                                       get_combinations(
                                    #                                           betas,
                                    #                                           default_wait_seconds)))))
    print(combinations)

    start_time = time.time()
    lossy_socket.sim = lossy_socket.SimulationParams(loss_rate=0.1, corruption_rate=0.1,
                                                     max_delivery_delay=0.1,
                                                     become_reliable_after=100000000.0)

    if len(sys.argv) < 4:
        print("usage is: python3 test.py [port1] [port2] [1|2]")
        print("First run with last argument set to 1, then with 2 (in two different terminals on the same machine")
        sys.exit(-1)

    # if sys.argv[1] == "1":
    #     host1(port1, port2)
    # elif sys.argv[1] == "2":
    #     host2(port2, port1)
    # else:
    #     print("Unexpected last argument: " + sys.argv[2])
    # print("TIME ELAPSED=%f" % (time.time() - start_time), "secs")


if __name__ == "__main__":
    main()
