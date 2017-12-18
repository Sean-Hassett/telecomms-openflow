"""
Name:          Sean Hassett

The Launcher is preconfigured with the list of routers that will be in the system
For each router it creates a Router object with the appropriate configuration as well as starting
the controller.
"""

import router
import controller

CONTROLLER_IP = "127.0.0.1"
CONTROLLER_PORT = 50000

ROUTER_IP = "127.0.0.1"

CLIENT_IP = "127.0.0.1"
CLIENT0_PORT = 10000
CLIENT1_PORT = 10100
CLIENT2_PORT = 10200
CLIENT3_PORT = 10300
CLIENT4_PORT = 10400

router_nodes = {'0':  ((ROUTER_IP, 40099), (ROUTER_IP, 40050), (ROUTER_IP, 40003)),
                '1':  ((ROUTER_IP, 40199), (ROUTER_IP, 40151), (ROUTER_IP, 40102), (ROUTER_IP, 40104)),
                '2':  ((ROUTER_IP, 40299), (ROUTER_IP, 40201), (ROUTER_IP, 40204), (ROUTER_IP, 40206)),
                '3':  ((ROUTER_IP, 40399), (ROUTER_IP, 40300), (ROUTER_IP, 40304), (ROUTER_IP, 40305)),
                '4':  ((ROUTER_IP, 40499), (ROUTER_IP, 40401), (ROUTER_IP, 40402), (ROUTER_IP, 40403),
                       (ROUTER_IP, 40408)),
                '5':  ((ROUTER_IP, 40599), (ROUTER_IP, 40503), (ROUTER_IP, 40507)),
                '6':  ((ROUTER_IP, 40699), (ROUTER_IP, 40602), (ROUTER_IP, 40609)),
                '7':  ((ROUTER_IP, 40799), (ROUTER_IP, 40752), (ROUTER_IP, 40705), (ROUTER_IP, 40708)),
                '8':  ((ROUTER_IP, 40899), (ROUTER_IP, 40804), (ROUTER_IP, 40807), (ROUTER_IP, 40810),
                       (ROUTER_IP, 40812)),
                '9':  ((ROUTER_IP, 40999), (ROUTER_IP, 40906), (ROUTER_IP, 40911), (ROUTER_IP, 40912)),
                '10': ((ROUTER_IP, 41099), (ROUTER_IP, 41008), (ROUTER_IP, 41013)),
                '11': ((ROUTER_IP, 41199), (ROUTER_IP, 41153), (ROUTER_IP, 41109), (ROUTER_IP, 41114)),
                '12': ((ROUTER_IP, 41299), (ROUTER_IP, 41208), (ROUTER_IP, 41209), (ROUTER_IP, 41214),
                       (ROUTER_IP, 41215)),
                '13': ((ROUTER_IP, 41399), (ROUTER_IP, 41310), (ROUTER_IP, 41315)),
                '14': ((ROUTER_IP, 41499), (ROUTER_IP, 41411), (ROUTER_IP, 41412)),
                '15': ((ROUTER_IP, 41599), (ROUTER_IP, 41554), (ROUTER_IP, 41512), (ROUTER_IP, 41513))}

router_neighbours = {'0':  (('E0', 1, (CLIENT_IP, CLIENT0_PORT)), (3, 2, (ROUTER_IP, 40300))),
                     '1':  (('E1', 1, (CLIENT_IP, CLIENT1_PORT)), (2, 2, (ROUTER_IP, 40201)),
                            (4, 3, (ROUTER_IP, 40401))),
                     '2':  ((1, 1, (ROUTER_IP, 40102)), (4, 2, (ROUTER_IP, 40402)), (6, 3, (ROUTER_IP, 40602))),
                     '3':  ((0, 1, (ROUTER_IP, 40003)), (4, 2, (ROUTER_IP, 40403)), (5, 3, (ROUTER_IP, 40503))),
                     '4':  ((1, 1, (ROUTER_IP, 40104)), (2, 2, (ROUTER_IP, 40204)), (3, 3, (ROUTER_IP, 40304)),
                            (8, 4, (ROUTER_IP, 40804))),
                     '5':  ((3, 1, (ROUTER_IP, 40305)), (7, 2, (ROUTER_IP, 40705))),
                     '6':  ((2, 1, (ROUTER_IP, 40206)), (9, 2, (ROUTER_IP, 40906))),
                     '7':  (('E2', 1, (CLIENT_IP, CLIENT2_PORT)), (5, 2, (ROUTER_IP, 40507)),
                            (8, 3, (ROUTER_IP, 40807))),
                     '8':  ((4, 1, (ROUTER_IP, 40408)), (7, 2, (ROUTER_IP, 40708)), (10, 3, (ROUTER_IP, 41008)),
                            (12, 4, (ROUTER_IP, 41208))),
                     '9':  ((6, 1, (ROUTER_IP, 40609)), (11, 2, (ROUTER_IP, 41109)), (12, 3, (ROUTER_IP, 41209))),
                     '10': ((8, 1, (ROUTER_IP, 40810)), (13, 2, (ROUTER_IP, 41310))),
                     '11': (('E3', 1, (CLIENT_IP, CLIENT3_PORT)), (9, 2, (ROUTER_IP, 40911)),
                            (14, 3, (ROUTER_IP, 41411))),
                     '12': ((8, 1, (ROUTER_IP, 40812)), (9, 2, (ROUTER_IP, 40912)), (14, 3, (ROUTER_IP, 41412)),
                            (15, 4, (ROUTER_IP, 41512))),
                     '13': ((10, 1, (ROUTER_IP, 41013)), (15, 2, (ROUTER_IP, 41513))),
                     '14': ((11, 1, (ROUTER_IP, 41114)), (12, 2, (ROUTER_IP, 41214))),
                     '15': (('E4', 1, (CLIENT_IP, CLIENT4_PORT)), (12, 2, (ROUTER_IP, 41215)),
                            (13, 3, (ROUTER_IP, 41315)))}

c = controller.Controller(CONTROLLER_IP, CONTROLLER_PORT)

for r in router_nodes:
    sock_addresses = []
    neighbours = []
    for address in router_nodes[r]:
        sock_addresses.append(address)
    for neighbour in router_neighbours[r]:
        neighbours.append(neighbour)
    router.Router(r, sock_addresses, neighbours)
