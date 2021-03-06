# Utils file for Middle-Out Compression
# © Johnathan Chiu, 2019

import array
import os


def positive_binary(num, bits=8):
    length = '{0:0' + str(bits) + 'b}'
    return length.format(num)


def positive_int(binary):
    return int(binary, 2)


def unsigned_int_list(binary, bits=8):
    return [int(binary[i:i+bits], 2) for i in range(0, len(binary), bits)]


def unsigned_bin_list(vals, bits=8):
    length = '{0:0' + str(bits) + 'b}'
    return ''.join([length.format(i) for i in vals])


def signed_bin(num, bits=8):
    s = bin(num & int("1" * bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)


def signed_int(binary, bits=8):
    binary = int(binary, 2)
    """compute the 2's complement of int value val"""
    if (binary & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        binary = binary - (1 << bits)  # compute negative value
    return binary  # return positive value as is


def signed_bin_list(intList, bits=8):
    def bindigits(val, bits=8):
        s = bin(val & int("1" * bits, 2))[2:]
        return ("{0:0>%s}" % (bits)).format(s)
    binary = ''
    for x in intList:
        binary += bindigits(x, bits=bits)
    return binary


def signed_int_list(binary, bits=8):
    def two_complement(binary, bits=8):
        binary = int(binary, 2)
        """compute the 2's complement of int value val"""
        if (binary & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            binary = binary - (1 << bits)  # compute negative value
        return binary  # return positive value as is
    intList = []
    for x in range(0, len(binary), bits):
        intList.append(two_complement(binary[x:x+bits], bits=bits))
    return intList


def nibble_int_low(eight_bit):
    return eight_bit >> 4


def nibble_int_high(eight_bit):
    return eight_bit & 0x0F


def nibble_list(eight_bit_list):
    four_bit = []; append = four_bit.append
    for i in eight_bit_list:
        append(nibble_int_low(i)); append(nibble_int_high(i))
    return four_bit


def nibble_to_bytes(nibble_list):
    bytes_list = []; append = bytes_list.append
    for i in range(0, len(nibble_list), 2):
        append(positive_int(positive_binary(nibble_list[i], bits=4) + positive_binary(nibble_list[i+1], bits=4)))
    return bytes_list


def unaryconverter(num):
    unary = ''
    for _ in range(num):
        unary += '1'
    unary += '0'
    return unary


def unaryToInt(unr):
    num = 0
    while unr[num] != '0':
        num += 1
    return 1 if num == 0 else num


def minimum_bits(num):
    if num == 0:
        return 1
    return num.bit_length()


def pad_stream(length):
    padding = 4 - (length % 8)
    if padding >= 0:
        return padding
    return 8 + padding


def remove_padding(stream):
    num_pad_bits = stream[-4:]
    stream = stream[:-4]
    num_pad = -1 * signed_int(num_pad_bits, bits=4) + len(stream)
    return stream[:num_pad]


def write_file_bits(bitstring, fileName=None):
    bit_strings = [bitstring[i:i + 8] for i in range(0, len(bitstring), 8)]
    byte_list = [int(b, 2) for b in bit_strings]
    filename = fileName + '.bin'
    with open(filename, 'wb') as f:
        f.write(bytearray(byte_list))


def write_file_bytes(bytes_list, fileName=None):
    with open(fileName, 'wb') as f:
        f.write(bytearray(bytes_list))


def read_file_bits(fileName):
    size = os.stat(fileName).st_size
    with open(fileName, 'rb') as f:
        bytes = f.read(int(size))
    return ''.join([positive_binary(b, bits=8) for b in bytes])


def read_file_bytes(fileName, bitdepth=8, partial=0):
    assert bitdepth == 4 or bitdepth == 8, "invalid bit depth argument"
    assert partial <= 1, "partial percentage greater than 100%"
    size = os.stat(fileName).st_size
    if partial: size *= partial
    with open(fileName, 'rb') as f:
        byte_stream = f.read(int(size))
    byte_stream = list(byte_stream)
    if not all(0 <= i <= 255 for i in byte_stream):
        byte_stream = [i+128 for i in byte_stream]
    if bitdepth == 8:
        return array.array('B', byte_stream)
    return nibble_list(byte_stream)


def convert_to_list(bitstring):
    bit_strings = [bitstring[i:i + 8] for i in range(0, len(bitstring), 8)]
    return [int(b, 2) for b in bit_strings]


def split_file(file_values, chunksize=32000):
    return [file_values[x:x+chunksize] for x in range(0, len(file_values), chunksize)]


def size_of_file(filename):
    return os.stat(filename).st_size

