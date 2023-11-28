# data = b"\x48\x41\x4Casdhajklfhadksjflhdaskjfghalskgjhdflgikuh\x46\x41\x48"
#
# start = data.find(b"\x48\x41\x4C\x46")
# end = data.find(b"\x46\x4C\x41\x48")
#
# print(start, end)
# print(data[start + 4:end])
import binascii


def mono_decode(mono_data: bytes) -> bytes:
    res_data = b""
    binary_sequence = bin(int(binascii.hexlify(mono_data), 16))[2:]
    for i in range(len(binary_sequence)):
        res_data += b"\xFF" if binary_sequence[i] == "1" else b"\x00"
    return res_data


byte_sequence = b'\x48\x41\x4Casdhajklfhadksjflhdaskjfghalskgjhdflgikuh\x46\x41\x48'
print(mono_decode(byte_sequence))
