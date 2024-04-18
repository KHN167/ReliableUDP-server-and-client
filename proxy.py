import socket
import sys
import random
import time
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL) #added so that ctl + c closes server

def validate_drop_chance(chance):
        if chance < 0.0 or chance > 100.0:
            print("Drop chance must be between 0 and 100")
            sys.exit(1)

def validate_delay_chance(chance):
        if chance < 0.0 or chance > 100.0:
            print("Delay chance must be between 0 and 100")
            sys.exit(1)

def validate_delay(min_value, max_value):
        if min_value < 0 or max_value < 0 or min_value > max_value:
            print("Invalid delay range.Min<Max")
            sys.exit(1)

def proxy(proxy_host, proxy_port, server_host, server_port, client_drop_chance, server_drop_chance, client_delay_chance, server_delay_chance, client_delay_min, client_delay_max, server_delay_min, server_delay_max):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as proxy_socket:
        proxy_socket.bind((proxy_host, proxy_port))
        print(f"Proxy is listening on {proxy_host}:{proxy_port}")

        while True:
            data, client_address = proxy_socket.recvfrom(1024)
            print(f"Proxy received data from {client_address}: {data.decode()}")

            # Simulate packet drop from client to proxy
            if random.random() < client_drop_chance / 100 :
                print("Packet dropped from client to proxy.")
                continue

            # Simulate packet delay from client to proxy
            if random.random() < client_delay_chance / 100:
                delay = random.randint(client_delay_min, client_delay_max)
                print(f"Packet delayed from client to proxy by {delay} ms.")
                time.sleep(delay / 1000)

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                server_socket.sendto(data, (server_host, server_port))
                print(f"Proxy sent data to server: {data.decode()}")

                response, _ = server_socket.recvfrom(1024)

            # Simulate packet drop from server to proxy
            if random.random() < server_drop_chance / 100:
                print("Packet dropped from server to proxy.")
                continue

            # Simulate packet delay from server to proxy
            if random.random() < server_delay_chance / 100:
                delay = random.randint(server_delay_min, server_delay_max)
                print(f"Packet delayed from server to proxy by {delay} ms.")
                time.sleep(delay / 1000)

            proxy_socket.sendto(response, client_address)
            print(f"Proxy sent response to {client_address}: {response.decode()}")

if __name__ == "__main__":
    if len(sys.argv) != 13:
        print("Usage: python proxy.py <proxy_host> <proxy_port> <server_host> <server_port> <client_drop_chance> <server_drop_chance> <client_delay_chance> <server_delay_chance> <client_delay_min> <client_delay_max> <server_delay_min> <server_delay_max>")
        sys.exit(1)

    proxy_host = sys.argv[1]
    proxy_port = int(sys.argv[2])
    server_host = sys.argv[3]
    server_port = int(sys.argv[4])
    client_drop_chance = float(sys.argv[5])
    server_drop_chance = float(sys.argv[6])
    client_delay_chance = float(sys.argv[7])
    server_delay_chance = float(sys.argv[8])
    client_delay_min = int(sys.argv[9])
    client_delay_max = int(sys.argv[10])
    server_delay_min = int(sys.argv[11])
    server_delay_max = int(sys.argv[12])

    validate_drop_chance(client_drop_chance)
    validate_drop_chance(server_drop_chance)
    validate_delay_chance(client_delay_chance)
    validate_delay_chance(server_delay_chance)
    validate_delay(client_delay_min, client_delay_max)
    validate_delay(server_delay_min, server_delay_max)

    proxy(proxy_host, proxy_port, server_host, server_port, client_drop_chance, server_drop_chance, client_delay_chance, server_delay_chance, client_delay_min, client_delay_max, server_delay_min, server_delay_max)
