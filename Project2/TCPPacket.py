import struct

len_sequence_number = 4
len_acknowledgement_number = 4
len_flags = 6


class TCPPacket:
    data_bytes = None
    sequence_number = None
    acknowledgement_number = None

    flags = [
        None, None, None, None, None, None
    ]

    def unpack(self, packet) -> None:
        packing_format = 'II6s' + str(len(packet) - len_sequence_number - len_acknowledgement_number - len_flags) + 's'
        self.sequence_number, self.acknowledgement_number, flag_bytes, self.data_bytes = struct.unpack(packing_format,
                                                                                                       packet)
        self.unpack_flags(flag_bytes)

    def pack(self, sequence_number: int = 0, acknowledgement_number: int = 0,
             urgent: bool = False, ack: bool = False, push: bool = False, reset: bool = False,
             syn: bool = False,
             fin: bool = False, data_bytes: bytes = b'') -> bytes:
        packing_format = 'II6s' + str(len(data_bytes)) + 's'

        self.sequence_number = sequence_number
        self.acknowledgement_number = acknowledgement_number
        self.flags = [urgent, ack, push, reset, syn, fin]
        self.data_bytes = data_bytes

        return struct.pack(packing_format, self.sequence_number, self.acknowledgement_number,
                           self.pack_flags(urgent, ack, push, reset, syn, fin),
                           self.data_bytes)

    @staticmethod
    def pack_flags(urgent: bool = False, ack: bool = False, push: bool = False, reset: bool = False,
                   syn: bool = False,
                   fin: bool = False) -> bytes:
        return (b'1' if urgent else b'0') + (b'1' if ack else b'0') + (b'1' if push else b'0') + (
            b'1' if reset else b'0') + (b'1' if syn else b'0') + (b'1' if fin else b'0')

    def unpack_flags(self, flag_bytes: bytes) -> None:
        self.flags = [True if flag == 49 else False for flag in flag_bytes]

    def __str__(self):
        return str(self.sequence_number) + " | " + str(self.acknowledgement_number) + '\n' + self.data_bytes.decode(
            'utf-8')

    def __eq__(self, other):
        return self.sequence_number == other.sequence_number and self.flags == other.flags
