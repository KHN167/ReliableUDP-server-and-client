import socket
import json


SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


ack = 0


received_seqs = set()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind((SERVER_IP, SERVER_PORT))

print('UDP server is listening...')

while True:

    data, client_address = server_socket.recvfrom(1024)

    print(f"Received message from {client_address}: {data.decode()}")


    parsed_data = json.loads(data)
    sequence_number = parsed_data['sequence_number']
    

    if sequence_number not in received_seqs:
        print("Sequence Number:", sequence_number)
        print("Acknowledgment Number:", ack)

        # Update set of received sequence numbers
        received_seqs.add(sequence_number)

        # Increment acknowledgment number
        ack += 1

        # Send acknowledgment back to the client
        acknowledgment = json.dumps({'ack': ack})
        server_socket.sendto(acknowledgment.encode(), client_address)
    else:
        server_socket.sendto(acknowledgment.encode(), client_address)
        # If the sequence number is a duplicate, ignore the message
        print("Duplicate sequence number received. Ignoring the message.")
