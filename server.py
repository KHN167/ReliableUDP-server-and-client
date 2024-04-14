import socket
import sys

SEQUENCE_NUMBER = 0

def main(server_host, server_port):
    server_address = (server_host, server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    
    print(f"Server listening on {server_address[0]}:{server_address[1]}")
    
    global SEQUENCE_NUMBER
    
    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Received message from client {client_address}: {message}")
        
        received_sequence_number = int(message.split()[-1])
        if received_sequence_number == SEQUENCE_NUMBER:
            server_socket.sendto(f"Ack {SEQUENCE_NUMBER}".encode(), client_address)
            print(f"Sent acknowledgment: Ack {SEQUENCE_NUMBER}")
            SEQUENCE_NUMBER += 1
        elif received_sequence_number < SEQUENCE_NUMBER:
            print("Duplicate packet received. Discarding.")
            server_socket.sendto(f"Ack {SEQUENCE_NUMBER-1}".encode(), client_address)
        else:
            print("Out-of-order packet received. Discarding.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    main(server_host, server_port)
