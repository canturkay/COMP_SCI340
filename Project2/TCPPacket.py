import hashlib
import struct

len_sequence_number = 4
len_acknowledgement_number = 4
len_flags = 2
len_checksum = 16


class TCPPacket:
    data_bytes = None
    sequence_number = None
    acknowledgement_number = None
    checksum = None

    ack = None
    fin = None

    def unpack(self, packet) -> None:
        packing_format = '16sII??' + str(
            len(packet) - len_sequence_number - len_acknowledgement_number - len_flags - len_checksum) + 's'
        self.checksum, self.sequence_number, self.acknowledgement_number, self.ack, self.fin, self.data_bytes = struct.unpack(
            packing_format,
            packet)

    def __init__(self, sequence_number: int = 0, acknowledgement_number: int = 0, ack: bool = False,
                 fin: bool = False, data_bytes: bytes = b''):
        self.sequence_number = sequence_number
        self.acknowledgement_number = acknowledgement_number

        self.data_bytes = data_bytes

        self.ack = ack
        self.fin = fin

    def pack(self) -> bytes:
        packing_format = 'II??' + str(len(self.data_bytes)) + 's'

        packet = struct.pack(packing_format, self.sequence_number, self.acknowledgement_number,
                             self.ack, self.fin,
                             self.data_bytes)

        self.checksum = self.get_checksum(packet)

        return self.checksum + packet

    @staticmethod
    def get_checksum(packet: bytes) -> bytes:
        return hashlib.md5(packet).digest()

    def __str__(self):
        return str(self.sequence_number) + " | " + str(self.acknowledgement_number) + '\n' + self.data_bytes.decode(
            'utf-8')

    def __eq__(self, other):
        return self.checksum == other.checksum
