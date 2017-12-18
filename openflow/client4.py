"""
Name:          Sean Hassett

Client4 "Eoin"
"""

import threading
import socket
import packet_utils


BUFFER_SIZE = 1024
PACKET_TYPE_CLIENT_MSG = 1

ROUTER_IP = "127.0.0.1"
ROUTER_PORT = 41554

CLIENT_IP = "127.0.0.1"
CLIENT0_PORT = 10000
CLIENT1_PORT = 10100
CLIENT2_PORT = 10200
CLIENT3_PORT = 10300
CLIENT4_PORT = 10400

clients = {'E0': (CLIENT_IP, CLIENT0_PORT),
           'E1': (CLIENT_IP, CLIENT1_PORT),
           'E2': (CLIENT_IP, CLIENT2_PORT),
           'E3': (CLIENT_IP, CLIENT3_PORT),
           'E4': (CLIENT_IP, CLIENT4_PORT)}

# frivolous
client_names = {'E0': 'Alan',
                'E1': 'Bill',
                'E2': 'Carl',
                'E3': 'Dave',
                'E4': 'Eoin'}


class Client:
    def __init__(self, host, port, r_host, r_port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.router_address = (r_host, r_port)

        print("USER: Eoin")
        try:
            threading.Thread(target=self.send_messages).start()
            threading.Thread(target=self.receive_messages).start()
        except KeyboardInterrupt:
            ''

    def send_messages(self):
        while True:
            message_out = bytes(input(""), "utf-8")

            have_client = False
            while not have_client:
                destination = input("Select a Client by entering a number:\nAlan[0], Bill[1], Carl[2], Dave[3]:\n")
                dest_client = 'E' + destination
                if dest_client not in clients or dest_client == 'E4':
                    print("Error, try again.\n")
                else:
                    have_client = True

            packet = packet_utils.create_packet(0, PACKET_TYPE_CLIENT_MSG, self.host, self.port,
                                                clients[dest_client][0], clients[dest_client][1], message_out)
            self.sock.sendto(packet, self.router_address)

    def receive_messages(self):
        while True:
            packet, address = self.sock.recvfrom(BUFFER_SIZE)
            unpacked = packet_utils.unpack(packet)
            if unpacked.packet_type == PACKET_TYPE_CLIENT_MSG:
                message_in = unpacked.data
                sender_address = (unpacked.source_ip, unpacked.source_port)
                sender = ''
                for name in client_names:
                    if clients[name] == sender_address:
                        sender = client_names[name]
                print(sender + ": " + message_in)


if __name__ == "__main__":
    Client(CLIENT_IP, CLIENT4_PORT, ROUTER_IP, ROUTER_PORT)
