import csv
import multiprocessing.pool
import random
import socket
import sys
import time

import test_packages.lossy_socket
from test_packages.streamer import Streamer

reserved_ports = []
test_results = []


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess


def receive(s, nums):
    expected = 0
    str_buf = ""
    while expected < nums:
        data = s.recv()
        # print("recv returned {%s}" % data.decode('utf-8'))
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
                # print("ERROR: got %s but was expecting %d" % (t, expected))
                sys.exit(-1)
            else:
                # we only received the first part of the number at the end
                # we must leave it in the buffer and read more.
                str_buf = t
                break


def host1(listen_port, remote_port, nums, alpha, beta, default_wait_seconds,
          sim: test_packages.lossy_socket.SimulationParams) -> test_packages.lossy_socket.SimulationStats:
    s = Streamer(dst_ip="localhost", dst_port=remote_port,
                 src_ip="localhost", src_port=listen_port)

    s.socket.sim = sim

    s.alpha = alpha
    s.beta = beta
    s.default_wait_seconds = default_wait_seconds

    receive(s, nums)

    # print("STAGE 1 TEST PASSED!")
    # send large chunks of data
    i = 0
    buf = ""
    while i < nums:
        buf += ("%d " % i)
        if len(buf) > 12345 or i == nums - 1:
            # print("sending {%s}" % buf)
            s.send(buf.encode('utf-8'))
            buf = ""
        i += 1
    s.close()
    # print("CHECK THE OTHER SCRIPT FOR STAGE 2 RESULTS.")

    return s.socket.stats.bytes_recv, s.socket.stats.bytes_sent, s.socket.stats.packets_recv, s.socket.stats.packets_sent


def host2(listen_port, remote_port, nums, alpha, beta, default_wait_seconds,
          sim: test_packages.lossy_socket.SimulationParams) -> test_packages.lossy_socket.SimulationStats:
    s = Streamer(dst_ip="localhost", dst_port=remote_port,
                 src_ip="localhost", src_port=listen_port)

    s.socket.sim = sim

    s.alpha = alpha
    s.beta = beta
    s.default_wait_seconds = default_wait_seconds

    # send small pieces of data
    for i in range(nums):
        buf = ("%d " % i)
        # print("sending {%s}" % buf)
        s.send(buf.encode('utf-8'))
    receive(s, nums)
    s.close()

    # print("STAGE 2 TEST PASSED!")

    return s.socket.stats.bytes_recv, s.socket.stats.bytes_sent, s.socket.stats.packets_recv, s.socket.stats.packets_sent


def get_available_port() -> int:
    curr_port = random.randrange(8000, 65535)
    while curr_port in reserved_ports or not test_port(curr_port):
        curr_port = random.randrange(8000, 65535)
    return curr_port


def test_port(port_num: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port_num))
    if result == 0:
        sock.close()
        return False
    else:
        reserved_ports.append(port_num)
        sock.close()
        return True


def test_async(nums, loss_rate, corruption_rate, max_delivery_delay, alpha, beta, default_wait_seconds) -> list:
    start_time = time.time()
    executor = MyPool(2)
    sim1 = test_packages.lossy_socket.SimulationParams(loss_rate=loss_rate, corruption_rate=corruption_rate,
                                                       max_delivery_delay=max_delivery_delay,
                                                       become_reliable_after=100000000.0)

    sim2 = test_packages.lossy_socket.SimulationParams(loss_rate=loss_rate, corruption_rate=corruption_rate,
                                                       max_delivery_delay=max_delivery_delay,
                                                       become_reliable_after=100000000.0)

    port_1 = get_available_port()
    port_2 = get_available_port()

    # print("TESTING ON PORTS", port_1, port_2, "with", nums, "nums")
    thread_1 = executor.apply_async(func=host1, args=(port_2, port_1, nums, alpha, beta, default_wait_seconds, sim1))
    thread_2 = executor.apply_async(func=host2, args=(port_1, port_2, nums, alpha, beta, default_wait_seconds, sim2))

    stats1_bytes_recv, stats1_bytes_sent, stats1_packets_recv, stats1_packets_sent = thread_1.get()
    stats2_bytes_recv, stats2_bytes_sent, stats2_packets_recv, stats2_packets_sent = thread_2.get()

    res = [nums, loss_rate, corruption_rate, max_delivery_delay, alpha, beta, default_wait_seconds,
           time.time() - start_time,
           stats1_packets_sent,
           stats1_packets_recv,
           stats1_bytes_sent,
           stats1_bytes_sent + (18 + 20 + 8) * stats2_packets_sent,
           stats1_bytes_recv,
           stats1_bytes_recv + (18 + 20 + 8) * stats2_bytes_recv,
           stats2_packets_sent,
           stats2_packets_recv,
           stats2_bytes_sent,
           stats2_bytes_sent + (18 + 20 + 8) * stats2_packets_sent,
           stats2_bytes_recv,
           stats2_bytes_recv + (18 + 20 + 8) * stats2_bytes_recv,
           ]

    executor.close()
    executor.join()

    return res


def write_test_results():
    with open('test_outputs.csv', 'w+', newline='') as file_writer:
        csv_writer = csv.writer(file_writer)
        csv_writer.writerows(test_results)


# loss_rates = [0.1, 0.2]
# corruption_rates = [0.1, 0.2]
# max_delivery_delays = [0.1, 0.2]
#
# alphas = [0.1, 0.2]
# betas = [0, 0.1, 0.25]
# default_wait_seconds_list = [0.0001, 0.001, 0.01]
#
# nums_list = [100, 1000, 10000]

loss_rates = [0.1, 0.3]
corruption_rates = [0.1, 0.3]
max_delivery_delays = [0.1, 0.3]
alphas = [0.1, 0.125, 0.2]
betas = [0, 0.1, 0.25]
default_wait_seconds_list = [0.01, 0.1]
nums_list = [100, 1000, 10000]


def get_combinations(list_1: list, list_2: list) -> list:
    res = []
    for item_1 in list_1:
        for item_2 in list_2:
            if isinstance(item_1, list) and isinstance(item_2, list):
                res.append(item_1 + item_2)
            elif isinstance(item_1, list):
                res.append(item_1 + [item_2])
            elif isinstance(item_2, list):
                res.append([item_1] + item_2)
            else:
                res.append([item_1, item_2])
    return res


def get_complete_combinations(lists) -> list:
    res = lists[0]
    for l in lists[1:]:
        res = get_combinations(res, l)

    return res


def main():

    if len(sys.argv) < 2:
        print("usage is: python3 custom_tests.py [num_processes]")
    combinations = get_complete_combinations(
        [loss_rates, corruption_rates, max_delivery_delays, alphas, betas, default_wait_seconds_list])

    num_processes = int(sys.argv[1])
    executor = MyPool(processes=num_processes)

    index = 0
    total_len = len(combinations) * len(nums_list)
    threads = []

    with open('test_outputs.csv', 'a+', newline='') as file_writer:
        csv_writer = csv.writer(file_writer)

        for nums in nums_list:
            for loss_rate, corruption_rate, max_delivery_delay, alpha, beta, default_wait_seconds in combinations:
                print(int(index / total_len * 100), '%  === ', len(threads))
                while len(threads) >= num_processes:
                    for thread in threads:
                        if thread.ready():
                            csv_writer.writerow(thread.get())
                            threads.remove(thread)
                            index += 1
                    time.sleep(0.1)
                test_thread = executor.apply_async(func=test_async,
                                                   args=(
                                                   nums, loss_rate, corruption_rate, max_delivery_delay, alpha, beta,
                                                   default_wait_seconds))
                threads.append(test_thread)

        for thread in threads:
            csv_writer.writerow(thread.get())

        executor.close()
        executor.join()

        print("TESTS COMPLETE")


if __name__ == "__main__":
    main()
