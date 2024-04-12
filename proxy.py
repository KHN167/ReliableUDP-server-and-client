import socket
import random
import time
import json

class Message:
    def __init__(self, sequence_number, ack_number, data):
        self.sequence_number = sequence_number
        self.ack_number = ack_number
        self.data = data

    def to_json(self):
        return json.dumps({
            'sequence_number': self.sequence_number,
            'ack_number': self.ack_number,
            'data': self.data
        })

    @staticmethod
    def from_json(json_data):
        parsed_data = json.loads(json_data)
        return Message(parsed_data['sequence_number'], parsed_data['ack_number'], parsed_data['data'])


class UDPProxyServer:
    def __init__(self, proxy_host, proxy_port, server_host, server_port, drop_probability=0.1, delay_probability=0.1, min_delay=50, max_delay=200):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.server_host = server_host
        self.server_port = server_port
        self.drop_probability = drop_probability
        self.delay_probability = delay_probability
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.proxy_socket.bind((self.proxy_host, self.proxy_port))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        print("Proxy server is running...")
        while True:
            data, client_address = self.proxy_socket.recvfrom(1024)
            
            print("Received data from client:", data.decode())
            if random.random() < self.drop_probability:
                print("Dropped packet from client")
                continue

            if random.random() < self.delay_probability:
                delay = random.randint(self.min_delay, self.max_delay) / 1000.0
                print("Delayed packet from client by", delay, "seconds")
                time.sleep(delay)

            self.server_socket.sendto(data, (self.server_host, self.server_port))
            response, _ = self.server_socket.recvfrom(1024)
            if random.random() < self.drop_probability:
                print("Dropped packet from server")
                continue

            if random.random() < self.delay_probability:
                delay = random.randint(self.min_delay, self.max_delay) / 1000.0
                print("Delayed packet from server by", delay, "seconds")
                time.sleep(delay)

            self.proxy_socket.sendto(response, client_address)

if __name__ == "__main__":
    proxy_host = '127.0.0.1'
    proxy_port = 5555
    server_host = '127.0.0.1'
    server_port = 12345

    proxy = UDPProxyServer(proxy_host, proxy_port, server_host, server_port)
    proxy.run()
