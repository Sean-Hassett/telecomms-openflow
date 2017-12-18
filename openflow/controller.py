"""
Name:          Sean Hassett

The Controller takes in packets from each router containing the configuration for that router
and builds a map of the system
It uses the map to calculate the shortest paths through the system and updates each router with
this information on request
"""

import socket
import threading
import dijkstra
import packet_utils
from time import sleep

BUFFER_SIZE = 1024

CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = 50000

PACKET_TYPE_HELLO = 0
PACKET_TYPE_CLIENT_MSG = 1
PACKET_TYPE_LINK_STATE_REQUEST = 2
PACKET_TYPE_LINK_STATE_UPDATE = 3


class Controller(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.router_addresses = {}
        self.route_table = {}
        self.stable = True  # indicates changes to the router network
        self.vertices = []
        self.edges = {}
        self.client_list = []

        t = threading.Thread(target=self.update_router_status)
        t.setDaemon(True)
        t.start()
        t = threading.Thread(target=self.listen)
        t.setDaemon(False)
        t.start()

    def update_router_status(self):
        """
        Routinely checks to see if the router network has been changed and if so,
        configures new routing information
        """
        while True:
            sleep(1)
            if not self.stable:
                self.configure_routes()
                self.stable = True

    def configure_routes(self):
        """
        Builds routemaps between each of the clients using Dijkstra's Algorithm
        """
        # put each permutation of known clients into route table
        self.route_table = {}
        for i in range(len(self.client_list)):
            for j in range(i + 1, len(self.client_list)):
                source = self.client_list[i]
                destination = self.client_list[j]
                route_name = source + "-" + destination
                self.route_table[route_name] = 0

        # run Dijkstra's Algorithm using each client as the source
        graph = (self.vertices, self.edges)
        shortest_paths = []
        for client in self.client_list:
            shortest_paths.append(dijkstra.get_shortest_path(graph, client))

        # use the results from DA to generate routes
        for route in self.route_table:
            source = route[:2]
            i = int(source[1])
            destination = route[-2:]

            temp_route = []
            temp_node = destination
            while temp_node != source:
                temp_node = shortest_paths[i][temp_node]
                # catching ValueError prevents the endpoint being added to the list, only routers are added, as desired
                try:
                    temp_route.append(int(temp_node))
                except ValueError:
                    ''
            self.route_table[route] = temp_route[::-1]

    def listen(self):
        while True:
            packet, address = self.sock.recvfrom(BUFFER_SIZE)
            unpacked = packet_utils.unpack(packet)
            packet_type = unpacked.packet_type

            # router initialisation information
            if packet_type == PACKET_TYPE_HELLO:
                self.stable = False
                neighbour_info = unpacked.data.split(",")
                r_number = neighbour_info[0]
                r_ip = unpacked.source_ip
                r_port = unpacked.source_port
                self.router_addresses[r_number] = (r_ip, r_port)

                self.vertices.append(r_number)
                self.edges[neighbour_info[0]] = {}
                for i in range(1, len(neighbour_info)):
                    self.edges[neighbour_info[0]][neighbour_info[i]] = 1
                    # assume any non-ints are clients, catch clients and add them to list
                    try:
                        int(neighbour_info[i])
                    except ValueError:
                        self.client_list.append(neighbour_info[i])
                        self.vertices.append(neighbour_info[i])
                        self.edges[neighbour_info[i]] = {r_number: 1}

            # route requests from routers
            if packet_type == PACKET_TYPE_LINK_STATE_REQUEST:
                route = unpacked.data
                if route in self.route_table:
                    router_path = self.route_table[route]
                else:
                    # reverse the route order and check again, return route in reverse
                    route = route[-2:] + "-" + route[:2]
                    if route in self.route_table:
                        router_path = self.route_table[route][::-1]
                    route = route[-2:] + "-" + route[:2]

                print("\nController sending route information...")
                print("{}: {}\n".format(route, router_path))
                for i in range(len(router_path) - 1):
                    r_ip = self.router_addresses[str(router_path[i])][0]
                    r_port = self.router_addresses[str(router_path[i])][1]
                    target_router = str(router_path[i + 1])
                    destination = route[-2:]
                    info = bytes(destination + target_router, "utf-8")
                    packet = packet_utils.create_packet(0, PACKET_TYPE_LINK_STATE_UPDATE, CONTROLLER_IP,
                                                        CONTROLLER_PORT, r_ip, r_port, info)
                    self.sock.sendto(packet, (r_ip, r_port))


if __name__ == "__main__":
    Controller(CONTROLLER_IP, CONTROLLER_PORT)
