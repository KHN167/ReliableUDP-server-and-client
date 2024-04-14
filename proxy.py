# udp_proxy.py
import socket
import sys

def proxy(proxy_host, proxy_port, server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as proxy_socket:
        proxy_socket.bind((proxy_host, proxy_port))
        print(f"Proxy is listening on {proxy_host}:{proxy_port}")

        while True:
            data, client_address = proxy_socket.recvfrom(1024)
            print(f"Proxy received data from {client_address}: {data.decode()}")

            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                server_socket.sendto(data, (server_host, server_port))
                print(f"Proxy sent data to server: {data.decode()}")

                response, _ = server_socket.recvfrom(1024)
                print(f"Proxy received response from server: {response.decode()}")

                proxy_socket.sendto(response, client_address)
                print(f"Proxy sent response to {client_address}: {response.decode()}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python udp_proxy.py <proxy_host> <proxy_port> <server_host> <server_port>")
        sys.exit(1)

    proxy_host = sys.argv[1]
    proxy_port = int(sys.argv[2])
    server_host = sys.argv[3]
    server_port = int(sys.argv[4])
    proxy(proxy_host, proxy_port, server_host, server_port)
