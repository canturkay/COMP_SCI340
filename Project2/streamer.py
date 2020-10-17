# do not import anything else from loss_socket besides LossyUDP
from lossy_socket import LossyUDP
# do not import anything else from socket except INADDR_ANY
from socket import INADDR_ANY

import struct
from TCPPacket import TCPPacket


class Streamer:
    last_sequence_number = 0

    receive_buffer = []

    def __init__(self, dst_ip, dst_port,
                 src_ip=INADDR_ANY, src_port=0):
        """Default values listen on all network interfaces, chooses a random source port,
           and does not introduce any simulated packet loss."""
        self.socket = LossyUDP()
        self.socket.bind((src_ip, src_port))
        self.dst_ip = dst_ip
        self.dst_port = dst_port

    def send(self, data_bytes: bytes) -> None:
        """Note that data_bytes can be larger than one packet."""
        chunk_size = 1024

        chunk_index = 0
        while chunk_index * chunk_size < len(data_bytes):
            chunk_start_index = chunk_index*chunk_size
            chunk_end_index = min(len(data_bytes), (chunk_index + 1) * chunk_size)

            packet = TCPPacket()
            res = packet.pack(self.last_sequence_number, data_bytes[chunk_start_index:chunk_end_index])
            self.last_sequence_number += 1
            packet.unpack(res)

            self.socket.sendto(res,
                               (self.dst_ip, self.dst_port))
            chunk_index += 1

        # Your code goes here!  The code below should be changed!

        # for now I'm just sending the raw application-level data in one UDP payload

    def recv(self) -> bytes:
        """Blocks (waits) if no data is ready to be read from the connection."""

        while len(self.receive_buffer) == 0 or \
                self.receive_buffer[0].sequence_number > self.last_sequence_number + 1:
            data, addr = self.socket.recvfrom()
            packet = TCPPacket()
            packet.unpack(data)

            self.receive_buffer.append(packet)
            self.receive_buffer.sort(key=self.sort_func)

        curr = self.receive_buffer.pop(0)
        self.last_sequence_number += 1
        print(curr.data_bytes)
        print(self.last_sequence_number)

        return curr.data_bytes

    @staticmethod
    def sort_func(e: TCPPacket): return e.sequence_number

    def close(self) -> None:
        """Cleans up. It should block (wait) until the Streamer is done with all
           the necessary ACKs and retransmissions"""
        # your code goes here, especially after you add ACKs and retransmissions.
        pass
