"""
Name:          Sean Hassett

The Router class creates Router instances.
Routers have multiple sockets corresponding to nodes which it uses to communicate with its neighbours
Routers are aware of which other routers or clients are neighbours to it and sends this information to
the controller at startup.
"""

import socket
import threading
import packet_utils
from time import sleep

BUFFER_SIZE = 1024

PACKET_TYPE_HELLO = 0
PACKET_TYPE_CLIENT_MSG = 1
PACKET_TYPE_LINK_STATE_REQUEST = 2
PACKET_TYPE_LINK_STATE_UPDATE = 3

CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = 50000

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


class Router(object):
    def __init__(self, r_number, sock_addresses, neighbours):
        self.r_number = r_number
        self.sock_addresses = sock_addresses

        self.sockets = []
        for i in range(len(sock_addresses)):
            self.sockets.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
            self.sockets[i].bind((sock_addresses[i][0], sock_addresses[i][1]))

        self.neighbours = {}
        self.neighbour_nodes = {}
        self.destinations = {}

        for neighbour in neighbours:
            self.neighbours[str(neighbour[0])] = neighbour[1]
            self.neighbour_nodes[str(neighbour[0])] = (neighbour[2][0], neighbour[2][1])

        # send configuration information to the controller
        neighbours_string = str(r_number) + ","
        for n in neighbours:
            neighbours_string += str(n[0]) + ","
        neighbours_string = bytes(neighbours_string[:-1], "utf-8")
        packet = packet_utils.create_packet(0, PACKET_TYPE_HELLO, self.sock_addresses[0][0], self.sock_addresses[0][1],
                                            CONTROLLER_IP, CONTROLLER_PORT, neighbours_string)
        self.sockets[0].sendto(packet, (CONTROLLER_IP, CONTROLLER_PORT))

        n = 0
        for sock in self.sockets:
            t = threading.Thread(target=self.receive_messages, args=(n, sock))
            t.setDaemon(True)
            t.start()
            n += 1

    def send_request(self, source_client, destination_client):
        """
        Takes a source and destination client and queries the controller for route information
        """
        route = bytes(source_client + "-" + destination_client, "utf-8")
        packet = packet_utils.create_packet(0, PACKET_TYPE_LINK_STATE_REQUEST, self.sock_addresses[0][0],
                                            self.sock_addresses[0][1], CONTROLLER_IP, CONTROLLER_PORT, route)
        self.sockets[0].sendto(packet, (CONTROLLER_IP, CONTROLLER_PORT))

    def receive_messages(self, node, sock):
        """
        Listens for incoming traffic
        Link State Updates cause the routing table to be updated
        Client messages are passed along with the route being requested if necessary
        """
        while True:
            packet, address = sock.recvfrom(BUFFER_SIZE)
            print(str(self.r_number) + ":" + str(node))
            unpacked = packet_utils.unpack(packet)

            if unpacked.packet_type == PACKET_TYPE_LINK_STATE_UPDATE:
                route_info = unpacked.data
                destination = route_info[:2]
                target_router = route_info[2:]
                self.destinations[destination] = target_router

            if unpacked.packet_type == PACKET_TYPE_CLIENT_MSG:
                source_address = (unpacked.source_ip, unpacked.source_port)
                source_client = ''
                for c in clients:
                    if clients[c] == source_address:
                        source_client = c

                destination_address = (unpacked.destination_ip, unpacked.destination_port)
                destination_client = ''
                for c in clients:
                    if clients[c] == destination_address:
                        destination_client = c

                if destination_client in self.neighbours:
                    self.sockets[self.neighbours[destination_client]].sendto(packet,
                                                                             self.neighbour_nodes[destination_client])
                    print("")
                else:
                    if destination_client not in self.destinations:
                        self.send_request(source_client, destination_client)
                        sleep(.1)  # give time to receive link state update

                    next_router = self.destinations[destination_client]
                    sending_socket = self.sockets[self.neighbours[next_router]]
                    receiving_node = self.neighbour_nodes[next_router]

                    sending_socket.sendto(packet, receiving_node)
