# do not import anything else from loss_socket besides LossyUDP
# do not import anything else from socket except INADDR_ANY
import time
from concurrent.futures import ThreadPoolExecutor
from socket import INADDR_ANY

from TCPPacket import TCPPacket
from lossy_socket import LossyUDP


class Streamer:
    send_sequence_number = 0
    receive_sequence_number = 0

    receive_buffer = {}
    send_buffer = {}

    self_half_closed = False
    remote_closed = False
    closed = False

    executor = None
    recv_thread = None
    send_thread = None

    last_fin_ack_sent = None

    chunk_size = 1446
    time_out_seconds = 0.25
    fin_grace_period = 2
    default_wait_seconds = 0.001

    _alpha = 0.1
    DevRTT = 0.01
    EstimatedRTT = 0.15

    def __init__(self, dst_ip, dst_port,
                 src_ip=INADDR_ANY, src_port=0):
        """Default values listen on all network interfaces, chooses a random source port,
           and does not introduce any simulated packet loss."""
        self.socket = LossyUDP()
        self.socket.bind((src_ip, src_port))
        self.dst_ip = dst_ip
        self.dst_port = dst_port

        self.executor = ThreadPoolExecutor(max_workers=2)
        self.recv_thread = self.executor.submit(self.recv_async)
        self.send_thread = self.executor.submit(self.send_async)

    def send(self, data_bytes: bytes) -> None:
        """Note that data_bytes can be larger than one packet."""

        chunk_index = 0
        while chunk_index * self.chunk_size < len(data_bytes):
            chunk_start_index = chunk_index * self.chunk_size
            chunk_end_index = min(len(data_bytes), (chunk_index + 1) * self.chunk_size)

            packet = TCPPacket(sequence_number=self.send_sequence_number,
                               data_bytes=data_bytes[chunk_start_index:chunk_end_index])

            self.send_buffer[self.send_sequence_number] = (packet, 0)

            self.send_sequence_number += 1
            chunk_index += 1

    def send_ack(self, acknowledgement_number: int):
        packet = TCPPacket(sequence_number=acknowledgement_number, ack=True)
        self.socket.sendto(packet.pack(), (self.dst_ip, self.dst_port))

    def send_fin(self, sequence_number: int):
        packet = TCPPacket(fin=True, sequence_number=sequence_number)
        self.send_buffer[packet.sequence_number] = (packet, time.time())

    def recv(self) -> bytes:
        """Blocks (waits) if no data is ready to be read from the connection."""

        while self.receive_sequence_number not in self.receive_buffer:
            time.sleep(self.default_wait_seconds)

        # curr = self.receive_buffer.pop(0)
        curr = self.receive_buffer[self.receive_sequence_number]
        del self.receive_buffer[self.receive_sequence_number]
        self.receive_sequence_number += 1

        return curr.data_bytes

    def send_async(self):
        while not self.self_half_closed:
            try:
                copy_send_buffer = self.send_buffer.copy()
                for val in copy_send_buffer:
                    if isinstance(self.send_buffer[val], tuple):
                        packet, time_sent = self.send_buffer[val]
                        if time_sent is not None:
                            if time.time() - time_sent > self.time_out_seconds:
                                self.socket.sendto(packet.pack(),
                                                   (self.dst_ip, self.dst_port))
                                self.send_buffer[packet.sequence_number] = (packet, time.time())
                        else:
                            del self.send_buffer[packet.sequence_number]
                        pass
            except Exception as e:
                # print("Sender died!")
                print(e)
            time.sleep(self.default_wait_seconds)
        return True

    def recv_async(self):
        while not self.closed:
            try:
                data, addr = self.socket.recvfrom()
                if data is not None and data != b'':
                    packet = TCPPacket()
                    packet.unpack(data)

                    calculated_checksum = packet.get_checksum(data[16:])
                    if calculated_checksum == packet.checksum:
                        if packet.ack:
                            ack_packet = TCPPacket(sequence_number=packet.sequence_number)
                            if packet.sequence_number % 20 == 0:
                                self.calculate_new_timeout(time.time() - self.send_buffer[packet.sequence_number][1])
                            self.send_buffer[packet.sequence_number] = (ack_packet, None)
                        elif packet.fin:
                            print("FIN RECEIVED", time.time())
                            self.send_ack(acknowledgement_number=packet.sequence_number)
                            self.last_fin_ack_sent = time.time()
                            # if not self.self_half_closed:
                            #     # print("REMOTE CLOSED")
                            #     self.remote_closed = True
                        else:
                            self.send_ack(acknowledgement_number=packet.sequence_number)
                            if packet.sequence_number not in self.receive_buffer:
                                self.receive_buffer[packet.sequence_number] = packet
            except Exception as e:
                # print("listener died!")
                print(e)
                self.remote_closed = True

        return True

    def close(self) -> None:
        """Cleans up. It should block (wait) until the Streamer is done with all
           the necessary ACKs and retransmissions"""

        while len(self.send_buffer) > 0:
            # print(self.send_buffer)
            time.sleep(self.default_wait_seconds)

        print("SENDING FIN")

        self.send_fin(sequence_number=self.send_sequence_number)
        self.send_sequence_number += 1

        while len(self.send_buffer) > 0:
            time.sleep(self.default_wait_seconds)

        print("FIN ACCEPTED", self.remote_closed)
        self.self_half_closed = True

        while not self.remote_closed:
            if self.last_fin_ack_sent is not None:
                if time.time() - self.last_fin_ack_sent > self.fin_grace_period:
                    print("FIN COMPLETE")
                    self.remote_closed = True
                else:
                    time.sleep(self.default_wait_seconds)

        self.closed = True
        self.socket.stoprecv()

        while not self.send_thread.done():
            self.send_thread.cancel()
            time.sleep(self.default_wait_seconds)

        while not self.recv_thread.done():
            self.recv_thread.cancel()
            time.sleep(self.default_wait_seconds)

        self.executor.shutdown()
        # your code goes here, especially after you add ACKs and retransmissions.
        pass

    def calculate_new_timeout(self, sample_rtt: float):
        self.EstimatedRTT = (1-self._alpha) * self.EstimatedRTT + self._alpha * sample_rtt
        self.time_out_seconds = self.EstimatedRTT + self.DevRTT * 4
        # print(self.time_out_seconds)
