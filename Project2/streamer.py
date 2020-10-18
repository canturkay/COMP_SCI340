# do not import anything else from loss_socket besides LossyUDP
# do not import anything else from socket except INADDR_ANY
import time
from concurrent.futures import ThreadPoolExecutor
from socket import INADDR_ANY

from TCPPacket import TCPPacket
from lossy_socket import LossyUDP


class Streamer:
    last_sequence_number = 0

    receive_buffer = {}
    ack_buffer = {}

    closed = None
    executor = None
    thread = None
    chunk_size = 16

    remote_closed = False

    def __init__(self, dst_ip, dst_port,
                 src_ip=INADDR_ANY, src_port=0):
        """Default values listen on all network interfaces, chooses a random source port,
           and does not introduce any simulated packet loss."""
        self.socket = LossyUDP()
        self.socket.bind((src_ip, src_port))
        self.dst_ip = dst_ip
        self.dst_port = dst_port

        self.closed = False
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.thread = self.executor.submit(self.recv_async)

    def send(self, data_bytes: bytes) -> None:
        """Note that data_bytes can be larger than one packet."""

        chunk_index = 0
        while chunk_index * self.chunk_size < len(data_bytes):
            chunk_start_index = chunk_index * self.chunk_size
            chunk_end_index = min(len(data_bytes), (chunk_index + 1) * self.chunk_size)

            last_sequence_number = self.last_sequence_number
            self.ack_buffer[last_sequence_number] = False

            packet_sent = time.time()

            while not self.ack_buffer[last_sequence_number]:
                packet = TCPPacket()
                res = packet.pack(sequence_number=last_sequence_number,
                                  data_bytes=data_bytes[chunk_start_index:chunk_end_index])

                if time.time() - packet_sent >= 0.25:
                    self.socket.sendto(res,
                                       (self.dst_ip, self.dst_port))
                    packet_sent = time.time()
                time.sleep(.01)

            del self.ack_buffer[last_sequence_number]
            self.last_sequence_number += 1

            chunk_index += 1

    def send_ack(self, acknowledgement_number: int):
        packet = TCPPacket()
        res = packet.pack(acknowledgement_number=acknowledgement_number, ack=True)
        self.socket.sendto(res, (self.dst_ip, self.dst_port))

    def send_fin(self, sequence_number: int):
        packet = TCPPacket()
        res = packet.pack(fin=True, sequence_number=sequence_number)
        self.socket.sendto(res, (self.dst_ip, self.dst_port))

    def recv(self) -> bytes:
        """Blocks (waits) if no data is ready to be read from the connection."""

        # while len(self.receive_buffer) == 0 or \
        #         self.receive_buffer[0].sequence_number > self.last_sequence_number:
        while len(self.receive_buffer) == 0 or \
                self.last_sequence_number not in self.receive_buffer:
            time.sleep(.01)

        # curr = self.receive_buffer.pop(0)
        curr = self.receive_buffer[self.last_sequence_number]
        del self.receive_buffer[self.last_sequence_number]
        self.last_sequence_number += 1

        return curr.data_bytes

    # @staticmethod
    # def sort_packets(e: TCPPacket):
    #     return e.sequence_number

    def recv_async(self):
        while not self.closed:
            try:
                data, addr = self.socket.recvfrom()
                if data is not None and data != b'':
                    packet = TCPPacket()
                    packet.unpack(data)

                    if packet.flags[1]:
                        self.ack_buffer[packet.acknowledgement_number] = True
                    elif packet.flags[5]:
                        print("FIN RECEIVED")
                        self.send_ack(acknowledgement_number=packet.sequence_number)
                        self.remote_closed = True
                    else:
                        calculated_checksum = packet.get_checksum(data[16:])
                        if calculated_checksum == packet.checksum:
                            self.send_ack(packet.sequence_number)
                            if packet.sequence_number not in self.receive_buffer:
                                self.receive_buffer[packet.sequence_number] = packet
                        else:
                            print(calculated_checksum, packet.checksum)
                else:
                    self.closed = True
            except Exception as e:
                print("listener died!")
                print(e)
                self.closed = True
        return True

    def close(self) -> None:
        """Cleans up. It should block (wait) until the Streamer is done with all
           the necessary ACKs and retransmissions"""

        fin_sequence_number = self.last_sequence_number
        self.last_sequence_number += 1

        fin_sent = time.time()
        self.ack_buffer[fin_sequence_number] = False

        while not self.ack_buffer[fin_sequence_number]:
            if time.time() - fin_sent >= 0.25:
                self.send_fin(sequence_number=fin_sequence_number)
                fin_sent = time.time()
            time.sleep(.01)

        del self.ack_buffer[fin_sequence_number]

        while not self.remote_closed:
            pass

        self.closed = True
        self.socket.stoprecv()

        while not self.thread.done():
            self.thread.cancel()

        self.executor.shutdown()
        # your code goes here, especially after you add ACKs and retransmissions.
        pass
