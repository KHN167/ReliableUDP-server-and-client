import time
import sys
import socket
import matplotlib.pyplot as plt

TIMEOUT = 5  # Timeout value in seconds
MAX_RETRIES = 100  # Maximum number of retries
SEQUENCE_NUMBER = 0
packets_sent = 0
acks_received = 0
packets_retransmitted = 0

def send_packet(sock, server_address, message):
    global SEQUENCE_NUMBER
    global packets_sent
    global acks_received
    global packets_retransmitted
    
    packet = f"{message} - Packet {SEQUENCE_NUMBER}".encode()
    packets_sent += 1
    sock.sendto(packet, server_address)
    print(f"Sent: {packet}")
    
    retries = 0
    while retries < MAX_RETRIES:
        start_time = time.time()
        while time.time() - start_time < TIMEOUT:
            try:
                data, _ = sock.recvfrom(1024)
                ack = int(data.decode().split()[-1])
                response = data.decode()
                if ack == SEQUENCE_NUMBER:
                    acks_received += 1
                    print(f"Acknowledgment received: {ack}")
                    SEQUENCE_NUMBER += 1
                    return True
            except socket.timeout:
                packets_retransmitted += 1
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

    # Plotting the statistics
    labels = ['Sent', 'Acknowledged', 'Retransmitted']
    values = [packets_sent, acks_received, packets_retransmitted]

    # Creating the bar plot
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color='lightgreen')
    plt.xlabel('Packet Types')
    plt.ylabel('Count')
    plt.title('Packet Statistics (Client)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_address> <server_port>")
    else:
        server_address = sys.argv[1]
        server_port = sys.argv[2]
        main(server_address, server_port)