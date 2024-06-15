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

arr1 = arr.array('i', [1, 1, 1])
print(len(arr1))




