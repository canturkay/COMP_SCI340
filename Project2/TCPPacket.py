import struct

len_sequence_number = 4

class TCPPacket:
    data_bytes = None
    sequence_number = 0

    def unpack(self, packet):
        packing_format = 'L' + str(len(packet) - len_sequence_number) + 's'
        self.sequence_number, self.data_bytes = struct.unpack(packing_format, packet)

    def pack(self, sequence_number: int, data_bytes: bytes) -> bytes:
        packing_format = 'L' + str(len(data_bytes)) + 's'
        self.data_bytes = data_bytes
        self.sequence_number = sequence_number
        print(sequence_number)
        return struct.pack(packing_format, self.sequence_number, self.data_bytes)

