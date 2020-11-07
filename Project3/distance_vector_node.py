from simulator.node import Node
import copy
import json
'''
from simulator.node import Node


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return -1
'''

class Distance_Vector_Edge:
    cost = None
    time = None
    path = []

    def __init__(self, cost: int, path: list, time: int):
        self.cost = cost
        self.path = path
        self.time = time

    def is_newer_than(self, other: int):
        return self.time > other

    def from_str(self, message: str):
        json_value = json.loads(message)
        self.from_map(json_value)

    def from_map(self, json_value):
        self.cost = int(json_value["cost"])
        self.path = int(json_value["path"])
        self.time = int(json_value["time"])

    def __str__(self):
        return json.dumps(
            self.as_dict()
        )

    def __repr__(self):
        return str(self)

    def as_dict(self):
        return {
            "cost": self.cost,
            "path": self.path,
            "time": self.time
        }


class Distance_Vector_Node(Node):
    edges = {}
    #src, destination, cost, path, time


    def __init__(self, id):
        super().__init__(id)

    # Return a string
    def __str__(self):
        message = {}
        for key, val in self.edges.items():
            message[
                str((tuple(key)[1], tuple(key)[0])) if tuple(key)[0] == self.id else str(tuple(key))] = val.as_dict()

        return json.dumps(message)

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        hops = [self.id, neighbor]
        if latency == -1:
            hops = []
        link = Distance_Vector_Edge()
        link.init(cost=latency, time=self.get_time(), hops=hops)
        self.edges[frozenset((self.id, neighbor))] = link

        self.broadcast_to_neighbors()

    def broadcast_to_neighbors(self):
        self.send_to_neighbors(str(self))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        _edges = json.loads(m)
        changed = False

        for str_key, value in _edges.items():
            key = tuple(map(int, str_key[1:-1].split(',')))
            # value = json.loads(str_value)
            link = Distance_Vector_Edge()
            link.from_map(value)
            changed = self.update_edge(source=key[0], destination=key[1], new_edge=link) or changed

        if changed:
            self.broadcast_to_neighbors()

    def update_edge(self, source: int, destination: int, new_edge: Distance_Vector_Edge()) -> bool:
        changed = False

        if (frozenset((source, destination)) in self.edges and new_edge.is_newer_than(
                self.edges[frozenset((source, destination))].time)) or frozenset((
                source, destination)) not in self.edges:
            link = Distance_Vector_Edge()
            link.__init__(cost=new_edge.cost, time=new_edge.time, hops=[])
            self.edges[frozenset((source, destination))] = link
            changed = True

        return changed

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return self.edges[frozenset(self.id, destination)][1][2]
