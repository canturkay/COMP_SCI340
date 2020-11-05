import datetime
import heapq
import json


from simulator.node import Node


class Link_State_Edge:
    cost = None
    time = None

    def init(self, cost: int, time: int):
        self.cost = cost
        self.time = time

    def is_newer_than(self, other: int):
        return self.time > other

    def from_str(self, message: str):
        json_value = json.loads(message)
        self.from_map(json_value)

    def from_map(self, json_value):
        self.cost = int(json_value["cost"])
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
            "time": self.time
        }


class Node_Heap_Object:
    node_id = None
    cost = None
    prev = []

    def __repr__(self):
        return str(self.node_id) + ": " + str(self.cost) + " - " + str(self.prev)

    def __init__(self, node_id: int, cost: int, prev: list):
        self.node_id = node_id
        self.cost = cost
        self.prev = prev

    def __lt__(self, other):
        return self.cost < other.cost


class Link_State_Node(Node):
    edges = {}

    def __init__(self, id):
        super().__init__(id)

    # Return a string
    def __str__(self):
        message = {}
        for key, val in self.edges.items():
            message[str((tuple(key)[1], tuple(key)[0])) if tuple(key)[0] == self.id else str(tuple(key))] = val.as_dict()

        return json.dumps(message)

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        link = Link_State_Edge()
        link.init(cost=latency, time=self.get_time())
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
            link = Link_State_Edge()
            link.from_map(value)
            changed = self.update_edge(source=key[0], destination=key[1], new_edge=link) or changed

        if changed:
            self.broadcast_to_neighbors()

    def update_edge(self, source: int, destination: int, new_edge: Link_State_Edge) -> bool:
        # src = source
        # dst = destination
        changed = False

        # if destination == self.id:
        #     src = destination
        #     dst = source
        # elif (destination, source) in self.edges:
        #     src = destination
        #     dst = source

        if (frozenset((source, destination)) in self.edges and new_edge.is_newer_than(self.edges[frozenset((source, destination))].time)) or frozenset((
                source, destination)) not in self.edges:
            link = Link_State_Edge()
            link.init(cost=new_edge.cost, time=new_edge.time)
            self.edges[frozenset((source, destination))] = link
            changed = True

        return changed

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        res, _ = self.dijkstra(destination)
        if res is not None:
            return res[0]
        else:
            return -1

    def dijkstra(self, destination: int):
        dist = {}
        q = []
        heapq.heappush(q, Node_Heap_Object(node_id=self.id, cost=0, prev=[]))
        dist[self.id] = 0

        while len(q) > 0:
            v = heapq.heappop(q)
            if v.node_id == destination:
                return v.prev, v.cost

            for key_frozen, val in self.edges.items():
                key = tuple(key_frozen)
                if val.cost < 0:
                    pass
                else:
                    neighbor_key = None
                    if key[0] == v.node_id:
                        neighbor_key = key[1]
                    elif key[1] == v.node_id:
                        neighbor_key = key[0]

                    if neighbor_key is not None:
                        if neighbor_key not in dist or val.cost + v.cost < dist[neighbor_key]:
                            heapq.heappush(q,
                                           Node_Heap_Object(node_id=neighbor_key, cost=val.cost + v.cost,
                                                            prev=v.prev + [neighbor_key]))
                            dist[neighbor_key] = val.cost + v.cost

        return None
