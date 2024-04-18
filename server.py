import sys
import signal
import socket
import matplotlib.pyplot as plt

signal.signal(signal.SIGINT, signal.SIG_DFL)  # Handle Ctrl+C to exit

SEQUENCE_NUMBER = 0
# Global variables to store counts
word_count = 0
char_count = 0
char_frequency = {}
packets_sent = 0
acks_received = 0
packets_retransmitted = 0

def process_message(message):
    global word_count, char_count, char_frequency
    message = message.lower()  # Convert message to lowercase for non-case sensitive processing
    
    # Update word count
    word_count += len(message.split())

    # Update character count (excluding spaces)
    char_count += sum(1 for c in message if c != ' ')

    # Update character frequency count
    for char in message:
        if char != ' ':
            char_frequency[char] = char_frequency.get(char, 0) + 1

def main(server_host, server_port):
    global word_count, char_count, char_frequency
    global packets_sent
    global acks_received
    global packets_retransmitted
    server_address = (server_host, server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    
    print(f"Server listening on {server_address[0]}:{server_address[1]}")
    
    global SEQUENCE_NUMBER

    try:
        while True:
            data, client_address = server_socket.recvfrom(1024)
            message = data.decode()
            print(f"Received message from client {client_address}: {message}")
            if message == '':
                response = f"Word count: {word_count}, Character count (excluding spaces): {char_count}, Frequency count: {char_frequency}"
                print(response)
                server_socket.sendto(
                    f"END OF TRANSMISSION\nHERE ARE THE RESULTS:\n{response}\nAck {SEQUENCE_NUMBER}".encode(),
                    client_address)
                word_count = 0
                char_count = 0
                char_frequency = {}
                print(f"Sent acknowledgment: Ack {SEQUENCE_NUMBER}")
                packets_sent += 1
                print("End of transmission")
                SEQUENCE_NUMBER = 0
            else:
                received_sequence_number = int(message.split()[-1])
                acks_received += 1
                if received_sequence_number == SEQUENCE_NUMBER:
                    server_socket.sendto(f"Ack {SEQUENCE_NUMBER}".encode(), client_address)
                    print(f"Sent acknowledgment: Ack {SEQUENCE_NUMBER}")
                    packets_sent += 1

                    SEQUENCE_NUMBER += 1
                    process_message(message)
                    update_graph(packets_sent, acks_received, packets_retransmitted)
                elif received_sequence_number < SEQUENCE_NUMBER:
                    print("Duplicate packet received. Discarding.")
                    packets_retransmitted += 1
                    update_graph(packets_sent, acks_received, packets_retransmitted)
                    server_socket.sendto(f"Ack {SEQUENCE_NUMBER - 1}".encode(), client_address)
                else:
                    print("Out-of-order packet received. Discarding.")
                    packets_retransmitted += 1
                    update_graph(packets_sent, acks_received, packets_retransmitted)
                    server_socket.sendto(f"Ack {SEQUENCE_NUMBER - 1}".encode(), client_address)
    except KeyboardInterrupt:
        print("Server is shutting down...")
        server_socket.close()
        generate_graph(packets_sent, acks_received, packets_retransmitted)

def generate_graph(packets_sent, acks_received, packets_retransmitted):
    labels = ['Packets Sent', 'Acks Received', 'Packets Retransmitted']
    values = [packets_sent, acks_received, packets_retransmitted]
    
    plt.bar(labels, values)
    plt.title('Network Statistics')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.show()

def update_graph(packets_sent, acks_received, packets_retransmitted):
    plt.clf()
    labels = ['Packets Sent', 'Acks Received', 'Packets Retransmitted']
    values = [packets_sent, acks_received, packets_retransmitted]
    
    plt.bar(labels, values)
    plt.title('Network Statistics')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.pause(1) 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    main(server_host, server_port)
