import socket
import json
import threading
import time

TIMEOUT = 5
seq = 0

ack = 0

class Message:
    def __init__(self, sequence_number, data, ack=False):
        self.sequence_number = sequence_number
        self.data = data
        self.ack = ack

    def to_json(self):
        return json.dumps({
            'sequence_number': self.sequence_number,
            'data': self.data,
            'ack': self.ack
        })
    



TIMEOUT = 4  # Timeout duration in seconds

def send_message(message):
    global ack

    # Start timer
    start_time = time.monotonic()

    while True:
        # Calculate the end time based on TIMEOUT
        end_time = start_time + TIMEOUT

        # Send the message to the proxy
        client_socket.sendto(message.encode(), (PROXY_IP, PROXY_PORT))
        ack += 1

        try:
            # Set a timeout for receiving the response
            client_socket.settimeout(10)

            # Receive response from server
            response, _ = client_socket.recvfrom(1024)

            print("Response from Server:", response.decode())




            

            # Reset the timeout to default
            client_socket.settimeout(None)

            return  # Exit the function after receiving the response

        except socket.timeout:
            # If a timeout occurs
            client_socket.sendto(message.encode(), (PROXY_IP, PROXY_PORT))
            print("Timeout occurred, retransmitting message:", message)

        # Check if the current time exceeds the end time
        if time.monotonic() >= end_time:
            client_socket.sendto(message.encode(), (PROXY_IP, PROXY_PORT))
            break  # Exit the outer loop if a timeout occurs without receiving a 

        




# Define proxy IP address and port
PROXY_IP = '127.0.0.1'
PROXY_PORT = 5555

start_time = time.time()

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)






while True:
    message_text = input("Enter message to send ('quit' to exit): ")

    if message_text.lower() == 'quit':
        break

    message = Message(seq, message_text, ack)

    json_message = message.to_json()


    send_message(json_message)

    seq += 1

client_socket.close()