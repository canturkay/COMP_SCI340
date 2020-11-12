import copy
import json
import math

from simulator.node import Node


class Distance_Vector_Edge:
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

    def __eq__(self, other):
        return self.cost == other.cost and self.path == other.path and self.time == other.time

    def as_dict(self):
        return {
            "cost": self.cost,
            "path": self.path,
            "time": self.time
        }


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.my_dvs = {}
        self.neighbor_dvs = {}
        self.link_costs = {}

    def __str__(self):
        message = {}
        for key, val in self.my_dvs.items():
            message[
                str((tuple(key)[1], tuple(key)[0])) if tuple(key)[0] == self.id else str(tuple(key))] = val.as_dict()

        return copy.deepcopy(json.dumps(message))

    def link_has_been_updated(self, neighbor, latency):
        if latency == -1:
            self.link_costs[neighbor] = (float('inf'), self.get_time())
        else:
            self.link_costs[neighbor] = (latency, self.get_time())

        self.recompute_dvs()

    def recompute_dvs(self):
        self.my_dvs = {}

        for neighbor, value in self.link_costs.items():
            cost = value[0]
            time = value[1]

            self.my_dvs[frozenset((self.id, neighbor))] = Distance_Vector_Edge(cost=cost, path=[self.id, neighbor],
                                                                               time=time)

        for key, dv in self.neighbor_dvs.items():
            source = tuple(key)[0]
            destination = tuple(key)[1]

            if source in self.link_costs and math.isfinite(self.link_costs[source][0]):
                self.recompute_single_dv(src=source, dst=destination, dv=dv)

            if destination in self.link_costs and math.isfinite(self.link_costs[destination][0]):
                self.recompute_single_dv(src=destination, dst=source, dv=dv)

        self.broadcast_to_neighbors()

    def recompute_single_dv(self, src: int, dst: int, dv: Distance_Vector_Edge):
        key = frozenset((self.id, dst))
        new_cost = dv.cost + self.link_costs[src][0]
        if key in self.my_dvs:
            if new_cost < self.my_dvs[key].cost:
                new_path = [self.id] + copy.deepcopy(dv.path)
                self.my_dvs[key] = Distance_Vector_Edge(cost=new_cost, path=new_path, time=dv.time)
        else:
            new_path = [self.id] + copy.deepcopy(dv.path)
            self.my_dvs[key] = Distance_Vector_Edge(cost=new_cost, path=new_path, time=dv.time)

    def broadcast_to_neighbors(self):
        self.send_to_neighbors(str(self))
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        _neighbor_dvs = json.loads(m)

        changed = False

        for str_key, value in _neighbor_dvs.items():
            key = tuple(map(int, str_key[1:-1].split(',')))
            source = key[0]
            destination = key[1]
            link = Distance_Vector_Edge(cost=value['cost'], path=value['path'], time=value['time'])

            changed = self.process_neighbor_dv(src=source, dst=destination, dv=link) or changed

        if changed:
            self.recompute_dvs()

    def process_neighbor_dv(self, src: int, dst: int, dv: Distance_Vector_Edge):
        key = frozenset((src, dst))

        if key in self.neighbor_dvs:
            if self.id in dv.path:
                del self.neighbor_dvs[key]
                return True

            if dv.time > self.neighbor_dvs[key].time:
                self.neighbor_dvs[key] = dv
                return True
            return False
        else:
            if self.id in dv.path:
                return False
            else:
                self.neighbor_dvs[key] = dv
                return True

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        # if self.id == 1 and destination == 4:
        #     print(" ")
        key = frozenset((self.id, destination))
        if key in self.my_dvs:
            if self.my_dvs[key].cost < float('inf'):
                return copy.deepcopy(self.my_dvs[key].path)[1]

        return -1
