import pytest
from pyredis.protocol import encode_message

from pyredis.protocol import extract_frame_from_buffer
from pyredis.types import (
    Array,
    BulkString,
    Error,
    Integer,
    SimpleString,
)


@pytest.mark.parametrize(
    "buffer, expected",
    [
        # Test invalid Message
        (b"PING\r\n", (None, 0)),
        # Test cases for Simple Strings
        (b"+Par", (None, 0)),
        (b"+OK\r\n", (SimpleString("OK"), 5)),
        (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
        # Test cases for Errors
        (b"-Err", (None, 0)),
        (b"-Error Message\r\n", (Error("Error Message"), 16)),
        (b"-Error Message\r\n+Other", (Error("Error Message"), 16)),
        # Test cases for Integers
        (b":10", (None, 0)),
        (b":100\r\n", (Integer(100), 6)),
        (b":100\r\n+OK", (Integer(100), 6)),
        # Test cases for Bulk Strings
        (b"$5\r\nHel", (None, 0)),
        (b"$5\r\nHello\r\n", (BulkString(b"Hello"), 11)),
        (b"$12\r\nHello, World\r\n", (BulkString(b"Hello, World"), 19)),
        (b"$12\r\nHello\r\nWorld\r\n", (BulkString(b"Hello\r\nWorld"), 19)),
        (b"$0\r\n\r\n", (BulkString(b""), 6)),
        (b"$-1\r\n", (BulkString(None), 5)),
        # Test case for Arrays
        (b"*0", (None, 0)),
        (b"*0\r\n", (Array([]), 4)),
        (b"*-1\r\n", (Array(None), 5)),
        (b"*2\r\n$5\r\nhello\r\n$5\r\n", (None, 0)),
        (
            b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n",
            (Array([BulkString(b"hello"), BulkString(b"world")]), 26),
        ),
        (
            b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n+OK",
            (Array([BulkString(b"hello"), BulkString(b"world")]), 26),
        ),
        (b"*3\r\n:1\r\n:", (None, 0)),
        (
            b"*3\r\n:1\r\n:2\r\n:3\r\n",
            (Array([Integer(1), Integer(2), Integer(3)]), 16),
        ),
        (
            b"*3\r\n:1\r\n:2\r\n:3\r\n+OK",
            (Array([Integer(1), Integer(2), Integer(3)]), 16),
        ),
    ],
)
def test_read_frame(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected


@pytest.mark.parametrize(
    "message", "expected",
    [
        (SimpleString("Hello"), b"+Hello\r\n"),
        (BulkString("Hi there. This is Redis"), b"$23\r\nHi there! This is Redis.\r\n"),
        (SimpleString(" "), b"+\r\n"),
        (Error("Error"), b"-Error\r\n"),
        (BulkString("Another bulk string encoding"), b"$28\r\nAnother bulk string encoding\r\n"),
        (Array([]), b"*0\r\n"),
        (Array(None), b"*-1\r\n"),
        (Array([SimpleString("Hello"), BulkString("Yet another Hello"), Integer(100)]), b"*3\r\n+Hello\r\n$Yet another Hello\r\n:100\r\n")
    ]
)

def test_encode_message(message, expected):
    encoded_message = encode_message(message)
    assert encoded_message == expected

def test_encode_simple_string():
    input = SimpleString("Hello")
    assert "+Hello\r\n".encode() == encode_message(input)