import socket
import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL) #added so that ctl + c closes server

SEQUENCE_NUMBER = 0
# Global variables to store counts
word_count = 0
char_count = 0
char_frequency = {}

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
    server_address = (server_host, server_port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)
    
    print(f"Server listening on {server_address[0]}:{server_address[1]}")
    
    global SEQUENCE_NUMBER
    
    while True:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode()
        print(f"Received message from client {client_address}: {message}")
        if message== '':
            response = f"Word count: {word_count}, Character count (excluding spaces): {char_count}, Frequency count: {char_frequency}"
            print(response)
            server_socket.sendto(f"Ack {SEQUENCE_NUMBER} END OF TRANSMISSION\nHERE ARE THE RESULTS:\n {response}".encode(), client_address)
            word_count = 0
            char_count = 0
            char_frequency = {}
            print(f"Sent acknowledgment: Ack {SEQUENCE_NUMBER}")
            print("End of transmission")
            SEQUENCE_NUMBER =0
        else:
            received_sequence_number = int(message.split()[-1])
            if received_sequence_number == SEQUENCE_NUMBER:
                server_socket.sendto(f"Ack {SEQUENCE_NUMBER}".encode(), client_address)
                print(f"Sent acknowledgment: Ack {SEQUENCE_NUMBER}")
                SEQUENCE_NUMBER += 1
                process_message(message)
            elif received_sequence_number < SEQUENCE_NUMBER:
                print("Duplicate packet received. Discarding.")
                server_socket.sendto(f"Ack {SEQUENCE_NUMBER-1}".encode(), client_address)
            else:
                print("Out-of-order packet received. Discarding.")
                server_socket.sendto(f"Ack {SEQUENCE_NUMBER-1}".encode(), client_address)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    main(server_host, server_port)
