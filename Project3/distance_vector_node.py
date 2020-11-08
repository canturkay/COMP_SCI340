import copy
import json

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

    # Return a string
    def __str__(self):
        message = {}
        for key, val in self.my_dvs.items():
            message[
                str((tuple(key)[1], tuple(key)[0])) if tuple(key)[0] == self.id else str(tuple(key))] = val.as_dict()

        return copy.deepcopy(json.dumps(message))

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if latency == -1 and neighbor in self.link_costs:
            del self.link_costs[neighbor]
            del self.my_dvs[frozenset((self.id, neighbor))]

            for key, dv in copy.deepcopy(self.my_dvs).items():
                if dv.path[1] == neighbor:
                    del self.my_dvs[key]
            for key, dv in copy.deepcopy(self.neighbor_dvs).items():
                if dv.path[0] == neighbor:
                    del self.neighbor_dvs[key]

        else:
            self.link_costs[neighbor] = latency
            if frozenset((self.id, neighbor)) in self.my_dvs and self.my_dvs[
                frozenset((self.id, neighbor))].cost < latency:
                pass
            else:
                self.my_dvs[frozenset((self.id, neighbor))] = Distance_Vector_Edge(cost=latency,
                                                                                   path=[self.id, neighbor],
                                                                                   time=self.get_time())

        self.recompute_my_dvs()
        self.broadcast_to_neighbors()

    def broadcast_to_neighbors(self):
        # self.send_to_neighbors(str(self))
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        _neighbor_dvs = json.loads(m)
        changed = False

        for str_key, value in _neighbor_dvs.items():
            key = tuple(map(int, str_key[1:-1].split(',')))
            # value = json.loads(str_value)
            link = Distance_Vector_Edge(cost=int(value['cost']), path=value['path'], time=int(value['time']))
            # link.from_map(value)
            if key[0] != self.id:
                changed = self.update_neighbor_dvs(key=key, new_dv=link) or changed

        if changed:
            self.recompute_my_dvs()
            self.broadcast_to_neighbors()

    def recompute_my_dvs(self):
        for key, dv in copy.deepcopy(self.neighbor_dvs).items():
            if self.id not in dv.path:
                source = tuple(key)[0]
                destination = tuple(key)[1]
                if source in self.link_costs:
                    src = source
                    dst = destination

                    self.recompute_single_dv(src=src, dst=dst, dv=dv)

                if destination in self.link_costs:
                    src = destination
                    dst = source

                    self.recompute_single_dv(src=src, dst=dst, dv=dv)

                if source not in self.link_costs and destination not in self.link_costs:
                    del self.neighbor_dvs[frozenset((source, destination))]

    def recompute_single_dv(self, src: str, dst: str, dv: Distance_Vector_Edge):
        new_cost = self.my_dvs[frozenset((self.id, src))].cost + dv.cost

        if frozenset((self.id, dst)) in self.my_dvs and self.dv_is_valid(self.my_dvs[frozenset((self.id, dst))]):
            if new_cost < self.my_dvs[frozenset((self.id, dst))].cost:
                new_dv = copy.deepcopy(dv)
                new_dv.cost += self.my_dvs[frozenset((self.id, src))].cost
                new_dv.path = self.my_dvs[frozenset((self.id, src))].path[:-1] + new_dv.path
                self.my_dvs[frozenset((self.id, dst))] = new_dv
            else:
                pass
        else:
            new_dv = copy.deepcopy(dv)
            new_dv.cost += self.my_dvs[frozenset((self.id, src))].cost
            new_dv.path = self.my_dvs[frozenset((self.id, src))].path[:-1] + new_dv.path
            self.my_dvs[frozenset((self.id, dst))] = new_dv

    def dv_is_valid(self, dv: Distance_Vector_Edge):
        if dv.path[0] == 3 and dv.path[-1] == 6:
            print(" ")
        return dv.path[1] in self.link_costs and self.id not in dv.path[1:]

    def update_neighbor_dvs(self, key: tuple, new_dv: Distance_Vector_Edge) -> bool:
        if self.id in new_dv.path:
            return False
        if frozenset(key) in self.neighbor_dvs:
            if new_dv.is_newer_than(self.neighbor_dvs[frozenset(key)].time):
                if new_dv.cost == self.neighbor_dvs[frozenset(key)].cost and new_dv.path == self.neighbor_dvs[
                    frozenset(key)].path:
                    self.neighbor_dvs[frozenset(key)].time = new_dv.time
                    return False
                else:
                    self.neighbor_dvs[frozenset(key)] = new_dv
                    return True
            else:
                return False
        else:
            self.neighbor_dvs[frozenset(key)] = new_dv

        return True

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if self.id == 1 and destination == 4:
            print(" ")
        if frozenset((self.id, destination)) in self.my_dvs:
            return self.my_dvs[frozenset((self.id, destination))].path[1]

        return -1
