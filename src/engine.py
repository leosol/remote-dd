import os
import socket
import logging
from abc import abstractmethod
from utils import get_file_size


class PyRemoteParty:
    def __init__(self, block_size, skip_count, read_count, ip_address, tcp_port, listen, password):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.block_size = block_size
        self.skip_count = skip_count
        self.read_count = read_count
        self.password = password
        if ip_address is None:
            self.ip_address = '0.0.0.0'
        else:
            self.ip_address = ip_address
        self.tcp_port = tcp_port
        self.listen = listen

    def start(self):
        if self.listen:
            self._create_server_socket()
        else:
            self._create_client_socket()
        self.perform_duty()

    @abstractmethod
    def perform_duty(self):
        raise NotImplementedError("Must be implemented")

    def _create_server_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.tcp_port))
        self.socket.listen()
        self.logger.info(f"Server listening on {self.ip_address}:{self.tcp_port}")
        conn, addr = self.socket.accept()
        self.connection = conn
        self.remote_addr = addr
        self.logger.info(f"Connected by {addr}")
        while True:
            data = self.recv_data()
            if not data:
                break
            message = data.decode('utf-8')
            self.logger.debug(f"Content received: {message}")
            if self.password == message:
                self.logger.info("Password match")
                self.send_data("okay".encode('utf-8'))
                break

    def _create_client_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, self.tcp_port))
        self.logger.info(f"Connected to server at {self.ip_address}:{self.tcp_port}")
        while True:
            self.send_data(self.password.encode('utf-8'))
            data = self.recv_data()
            self.logger.debug(f"Received: {data.decode('utf-8')}")
            if "okay" == data.decode('utf-8'):
                self.logger.info("Password matched")
                break

    def send_data(self, data):
        if self.listen:
            self.connection.sendall(data)
        else:
            self.socket.sendall(data)

    def recv_data(self):
        if self.listen:
            data = self.connection.recv(self.block_size)
            return data
        else:
            data = self.socket.recv(self.block_size)
            return data

class PyRemoteDDServer(PyRemoteParty):
    def __init__(self, input_file, block_size, skip_count, read_count, ip_address, tcp_port, listen, password):
        super().__init__(block_size=block_size, skip_count=skip_count, read_count=read_count, ip_address=ip_address,
                         tcp_port=tcp_port, listen=listen, password=password)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.input_file = input_file

    def perform_duty(self):
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"File does not exists: {self.input_file}")
        already_sent_bytes_str = self.recv_data().decode('utf-8')
        already_sent_bytes_int = int(already_sent_bytes_str)
        if self.skip_count == 0:
            skip_count = int(already_sent_bytes_int/self.block_size)
        else:
            skip_count = self.skip_count
        with open(self.input_file, 'rb') as fp:
            read_count = 0
            while True:
                position = skip_count*self.block_size + read_count*self.block_size
                fp.seek(position)
                read_count = read_count + 1
                read_bytes = fp.read(self.block_size)
                self.send_data(read_bytes)
                if read_count % (1024 * 1024) == 0:
                    print(".", end="")


class PyRemoteDDClient(PyRemoteParty):
    def __init__(self, output_file, block_size, skip_count, read_count, ip_address, tcp_port, listen, password):
        super().__init__(block_size=block_size, skip_count=skip_count, read_count=read_count, ip_address=ip_address,
                         tcp_port=tcp_port, listen=listen, password=password)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.output_file = output_file

    def perform_duty(self):
        already_recv_bytes = get_file_size(self.output_file)
        self.logger.info(f"Already received {already_recv_bytes}")
        self.logger.info("Preparing for data download")
        self.send_data(str(already_recv_bytes).encode('utf-8'))
        count = 0
        with open(self.output_file, 'ab') as fp:
            while True:
                data = self.recv_data()
                count = count + 1
                fp.write(data)
                fp.flush()
                if count % (1024*1024) == 0:
                    print(".", end="")


