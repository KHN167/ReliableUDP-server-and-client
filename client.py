import socket
import time
import sys

TIMEOUT = 5  # Timeout value in seconds
MAX_RETRIES = 3  # Maximum number of retries
SEQUENCE_NUMBER = 0

def send_packet(sock, server_address, message):
    global SEQUENCE_NUMBER
    
    packet = f"{message} - Packet {SEQUENCE_NUMBER}".encode()
    sock.sendto(packet, server_address)
    print(f"Sent: {packet}")
    
    retries = 0
    while retries < MAX_RETRIES:
        start_time = time.time()
        while time.time() - start_time < TIMEOUT:
            try:
                data, _ = sock.recvfrom(1024)
                ack = int(data.decode().split()[1])
                if ack == SEQUENCE_NUMBER:
                    print(f"Acknowledgment received: {ack}")
                    SEQUENCE_NUMBER += 1
                    return True
            except socket.timeout:
                print("Timeout occurred. Resending packet.")
                sock.sendto(packet, server_address)
                print(f"Resent: {packet}")
                break
        
        retries += 1
    
    print("Maximum retries reached. Exiting.")
    return False

def main(server_address, server_port):
    server_address = (server_address, int(server_port))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)
    
    while True:
        message = input("Enter a message to send to the server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        
        # Attempt to send the message with retransmission until acknowledgment is received
        if not send_packet(client_socket, server_address, message):
            print("Failed to send the message. Exiting.")
            break

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_address> <server_port>")
    else:
        server_address = sys.argv[1]
        server_port = sys.argv[2]
        main(server_address, server_port)
