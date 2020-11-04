import datetime
import heapq
import json

from simulator.node import Node


class Link_State_Edge:
    cost = None
    time = None

    def init(self, cost: int, time: datetime.datetime):
        self.cost = cost
        self.time = time

    def is_newer_than(self, other: datetime.datetime):
        return self.time < other

    def from_str(self, message: str):
        json_value = json.loads(message)
        self.from_map(json_value)

    def from_map(self, json_value):
        self.cost = int(json_value["cost"])
        self.time = datetime.datetime.strptime(json_value["time"], '%Y-%m-%d %H:%M:%S.%f')

    def __str__(self):
        return json.dumps(
            {
                "cost": self.cost,
                "time": str(self.time)
            }
        )


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
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if latency > -1:
            if (self.id, neighbor) not in self.edges:
                link = Link_State_Edge()
                link.init(cost=latency, time=datetime.datetime.now())
                self.edges[(self.id, neighbor)] = link
                self.broadcast_to_neighbors()
            else:
                # if not self.edges[(self.id, neighbor)].is_newer_than(datetime.datetime.now()):
                link = Link_State_Edge()
                link.init(cost=latency, time=datetime.datetime.now())
                self.edges[(self.id, neighbor)] = link
                self.broadcast_to_neighbors()
        else:
            if (self.id, neighbor) in self.edges:
                del self.edges[(self.id, neighbor)]
                self.broadcast_to_neighbors()

    def broadcast_to_neighbors(self):
        message = {}
        for key, val in self.edges.items():
            message[str(key)] = str(val)
        self.send_to_neighbors(json.dumps(message))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        edges = json.loads(m)
        changed = False

        for str_key, str_value in edges.items():
            key = tuple(map(int, str_key[1:-1].split(',')))
            value = json.loads(str_value)
            link = Link_State_Edge()
            link.from_map(value)
            changed = self.update_edge(source=key[0], destination=key[1], new_edge=link) or changed

        if changed:
            self.broadcast_to_neighbors()

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        res = self.dijkstra(destination)
        if res:
            return res[0]
        else:
            return -1

    def dijkstra(self, destination: int) -> list:
        dist = {}
        q = [Node_Heap_Object(node_id=self.id, cost=0, prev=[])]
        dist[self.id] = 0
        heapq.heapify(q)

        while len(q) > 0:
            v = heapq.heappop(q)
            if v.node_id == destination:
                return v.prev

            for key, val in self.edges.items():
                neighbor_key = None
                if key[0] == v.node_id and (key[1] not in dist or dist[key[1]] > val.cost + v.cost):
                    neighbor_key = key[1]
                elif key[1] == v.node_id and (key[0] not in dist or dist[key[0]] > val.cost + v.cost):
                    neighbor_key = key[0]

                if neighbor_key:
                    heapq.heappush(q,
                                   Node_Heap_Object(node_id=neighbor_key, cost=val.cost + v.cost,
                                                    prev=v.prev + [neighbor_key]))
                    dist[neighbor_key] = val.cost + v.cost

        return None

    def update_edge(self, source: int, destination: int, new_edge: Link_State_Edge) -> bool:
        src = source
        dst = destination
        changed = False

        if destination == self.id:
            src = destination
            dst = source

        if (dst, src) in self.edges:
            self.edges[(src, dst)] = self.edges[(dst, src)]
            del self.edges[(dst, src)]

        if ((src, dst) in self.edges and new_edge.is_newer_than(self.edges[(src, dst)].time)) or (
                src, dst) not in self.edges:
            link = Link_State_Edge()
            link.init(cost=new_edge.cost, time=new_edge.time)
            self.edges[(src, dst)] = link
            changed = True

        return changed
