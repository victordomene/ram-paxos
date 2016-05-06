import select
import socket

class ClientDead(Exception):
    def __str__(self):
        return "I don't see dead people. And the client is dead."

class ServerDead(Exception):
    def __str__(self):
        return "I don't see dead people. And the server is dead."

##################################
### Real Data Transfer Protocol
##################################
#
# Magic number (1 byte) / Version (1 byte) / Status (1 byte)
# Length (1 byte) / Message (Length bytes)

RDTP_HEADER_LENGTH = 4
RDTP_MAGIC = unichr(0x42)
RDTP_VERSION = unichr(2)
ARG_LEN_MAX = 256

RDTP_MALFORMED = -55

def recv_message(sock):
    # get the first 3 bytes which are supposed to be part of the preamble
    header = recv_nbytes(sock, RDTP_HEADER_LENGTH)
    assert(len(header) == RDTP_HEADER_LENGTH)

    magic, version, status, msg_len = header[0], header[1], header[2], header[3]

    # Malformed message
    if magic != RDTP_MAGIC or version != RDTP_VERSION:
    	print header
    	return RDTP_MALFORMED, ""

    msg_len = ord(msg_len)

    # Wrong message length
    if msg_len < 0 or msg_len > ARG_LEN_MAX:
    	return RDTP_MALFORMED, ""

    # read in the expected message
    message = recv_nbytes(sock, msg_len)
    status_code = ord(status)

    return status_code, message

def recv(sock):
    status, message = recv_message(sock)
    args = message.split(':')
    return status, args

def send(sock, status, *args):
    send_message(sock, status, ':'.join(args))

def send_message(sock, status, message):
    msg_len = len(message)
    if msg_len > ARG_LEN_MAX:
    	print 'Message too long'
    	return False

    # Constructs RDTP message
    to_send = RDTP_MAGIC + RDTP_VERSION + unichr(status) + unichr(msg_len)
    to_send += message
    assert(len(to_send) == RDTP_HEADER_LENGTH + msg_len)

    # Sends the actual message
    try:
        sock.sendall(to_send)
    except:
        raise ServerDead


def recv_nbytes(sock, n):
    bytes_received = 0
    received = ""
    # keep on readin' until we get what we expected
    while bytes_received < n:
        ready_to_read,_,_ = select.select([sock],[],[])
        data = sock.recv(1, socket.MSG_PEEK)

        if len(data) == 0:
            raise ClientDead
        else:
            assert(ready_to_read != [])
            new_recv = sock.recv(n - bytes_received)
            bytes_received += len(new_recv)
            received += new_recv
    assert(bytes_received == len(received))
    return received

