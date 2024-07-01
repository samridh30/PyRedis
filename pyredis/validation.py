"""_MSG_SEPARATOR = b"\r\n"
_MSG_SEPARATOR_SIZE = len(_MSG_SEPARATOR)

def extract_frame_from_buffer(buffer):
    separator = buffer.find(_MSG_SEPARATOR)
    payload = buffer[1:separator].decode()
    print(payload)
    print(separator)

length = int(payload)

for _ in range(length):
next_item, length = extract_frame_from_buffer(
                        buffer[separator + _MSG_SEPARATOR_SIZE :])



buffer = b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
#extract_frame_from_buffer(buffer)

separator = buffer.find(_MSG_SEPARATOR)
print("This is separator:" , separator)

payload = buffer[1:separator].decode()
print(payload)
length  = int(payload)

print(length)
payload2 = buffer[0:separator].decode()

#length = int(payload)

print()
print(payload)
print(payload2)

"""
import array as arr
from dataclasses import dataclass

#arr1 = arr.array('i', [1, 1, 1])
#print(len(arr1))
"""
from pyredis.types import Array, BulkString

command = "1782.334.5> Hello Redis"

def encode_command(command):
    return Array([BulkString(p) for p in command.split()])

print(encode_command(command))  """
"""from protocol import encode_message, extract_frame_from_buffer
from pyredis.types import Array, BulkString
buffer = b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n"
frame, frame_size = extract_frame_from_buffer(buffer)

if frame:
    buffer = buffer[frame_size:]
    if isinstance(frame, Array):
        for count, item in enumerate(frame.data):
            print(f'{count + 1} "{item.as_str()}"')
    else:
        print(frame.as_str())
        """







