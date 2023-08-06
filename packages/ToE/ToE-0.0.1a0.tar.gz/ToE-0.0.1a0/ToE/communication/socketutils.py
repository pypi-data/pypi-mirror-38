import socket
import pickle
import struct


def recvall(sock, length):
    data = b''
    if type(length) is bytes:
        length = struct.unpack('>I', length)[0]
    while len(data) < length:
        data_part = sock.recv(length - len(data))
        if not data_part:
            return None
        data += data_part
    return data


def send_tensor(sock, tensor):
    tensor = pickle.dumps(tensor)
    tensor = struct.pack('>I', len(tensor)) + tensor
    sock.sendall(tensor)


def get_grad(sock):
    leng = recvall(sock, 4)
    grad = recvall(sock, leng)
    return pickle.loads(grad)


def get_tensor(sock):
    leng = recvall(sock, 4)
    tensor = recvall(sock, leng)
    return pickle.loads(tensor)


def send_grad(sock, grad):
    grad = pickle.dumps(grad)
    grad = struct.pack('>I', len(grad)) + grad
    sock.sendall(grad)

