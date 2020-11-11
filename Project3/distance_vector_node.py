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
            self.link_costs[neighbor] = (float('inf'), self.get_time())
            # self.my_dvs[frozenset((self.id, neighbor))] = Distance_Vector_Edge(cost=float('inf'),
            #                                                                    path=[self.id, neighbor],
            #                                                                    time=self.get_time())

            # for key, dv in copy.deepcopy(self.my_dvs).items():
            #     if dv.path[1] == neighbor:
            #         dv.cost = float('inf')
            #         dv.time = self.get_time()
            #         self.my_dvs[key] = dv
            for key, dv in copy.deepcopy(self.neighbor_dvs).items():
                if dv.path[0] == neighbor:
                    del self.neighbor_dvs[key]

        else:
            self.link_costs[neighbor] = (latency, self.get_time())
            if frozenset((self.id, neighbor)) in self.my_dvs and \
                    self.my_dvs[frozenset((self.id, neighbor))].cost < latency:
                pass
            else:
                self.my_dvs[frozenset((self.id, neighbor))] = Distance_Vector_Edge(cost=latency,
                                                                                   path=[self.id, neighbor],
                                                                                   time=self.get_time())

        self.recompute_my_dvs()
        self.broadcast_to_neighbors()

    def broadcast_to_neighbors(self):
        self.send_to_neighbors(str(self))
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        _neighbor_dvs = json.loads(m)

        changed = False
        if m == '{"(2, 3)": {"cost": 5, "path": [3, 2], "time": 2}, "(1, 3)": {"cost": 7, "path": [3, 1], "time": 3}, "(6, 3)": {"cost": Infinity, "path": [3, 6], "time": 21}, "(5, 3)": {"cost": 10000005, "path": [3, 2, 5], "time": 9}, "(4, 3)": {"cost": 10000007, "path": [3, 1, 4], "time": 8}}':
            print("YO")

        # neighbor = next(iter(_neighbor_dvs.values()))['path'][0]
        # if neighbor == 5 and self.id == 2:
        #     print("YP")
        # for key, value in copy.deepcopy(self.neighbor_dvs).items():
        #     if value.path[0] == neighbor:
        #         del self.neighbor_dvs[key]
        #
        # for key, value in copy.deepcopy(self.my_dvs).items():
        #     if value.path[1] == neighbor:
        #         del self.my_dvs[key]

        for str_key, value in _neighbor_dvs.items():
            key = tuple(map(int, str_key[1:-1].split(',')))
            # value = json.loads(str_value)
            link = Distance_Vector_Edge(cost=value['cost'], path=value['path'], time=value['time'])

            # link.from_map(value)
            # if key[0] != self.id and key[1] != self.id:
            changed = self.update_neighbor_dvs(key=key, new_dv=link) or changed

        if changed:
            self.recompute_my_dvs()
            self.broadcast_to_neighbors()

    def recompute_my_dvs(self):
        self.my_dvs = {}

        for key, value in self.link_costs.items():
            if not math.isinf(value[0]):
                self.my_dvs[frozenset((self.id, key))] = Distance_Vector_Edge(cost=value[0], path=[self.id, key],
                                                                             time=value[1])

        for key, dv in copy.deepcopy(self.neighbor_dvs).items():
            if self.id not in dv.path:
                source = tuple(key)[0]
                destination = tuple(key)[1]

                if (source not in self.link_costs or self.link_costs[source][0] == float('inf')) and (
                        destination not in self.link_costs or self.link_costs[destination][0] == float('inf')):
                    # del self.neighbor_dvs[frozenset((source, destination))]
                    pass
                else:
                    if source in self.link_costs:
                        src = source
                        dst = destination

                        res = self.recompute_single_dv(src=src, dst=dst, dv=dv)
                        if res:
                            self.my_dvs[frozenset((self.id, dst))] = res

                    if destination in self.link_costs:
                        src = destination
                        dst = source

                        res = self.recompute_single_dv(src=src, dst=dst, dv=dv)
                        if res:
                            self.my_dvs[frozenset((self.id, dst))] = res

    def recompute_single_dv(self, src: str, dst: str, dv: Distance_Vector_Edge) -> Distance_Vector_Edge:
        new_cost = self.my_dvs[frozenset((self.id, src))].cost + dv.cost

        if math.isinf(new_cost):
            return None

        if frozenset((self.id, dst)) in self.my_dvs and self.dv_is_valid(self.my_dvs[frozenset((self.id, dst))]):
            if new_cost < self.my_dvs[frozenset((self.id, dst))].cost:
                new_dv = copy.deepcopy(dv)
                new_dv.cost += self.my_dvs[frozenset((self.id, src))].cost
                new_dv.path = self.my_dvs[frozenset((self.id, src))].path[:-1] + new_dv.path
                return new_dv
            else:
                return self.my_dvs[frozenset((self.id, dst))]
        else:
            new_dv = copy.deepcopy(dv)
            new_dv.cost += self.my_dvs[frozenset((self.id, src))].cost
            new_dv.path = self.my_dvs[frozenset((self.id, src))].path[:-1] + new_dv.path
            return new_dv

    def dv_is_valid(self, dv: Distance_Vector_Edge):
        return self.id not in dv.path[1:] and dv.path[1] in self.link_costs and self.link_costs[dv.path[1]][0] < float(
            'inf')

    def update_neighbor_dvs(self, key: tuple, new_dv: Distance_Vector_Edge) -> bool:
        if frozenset(key) in self.neighbor_dvs:
            if math.isinf(new_dv.cost) or self.id in new_dv.path:
                del self.neighbor_dvs[frozenset(key)]
                return True

            if new_dv.time > self.neighbor_dvs[frozenset(key)].time:
                if new_dv.cost == self.neighbor_dvs[frozenset(key)].cost and new_dv.path == \
                        self.neighbor_dvs[frozenset(key)].path:
                    self.neighbor_dvs[frozenset(key)].time = new_dv.time
                    return False
                else:
                    self.neighbor_dvs[frozenset(key)] = new_dv
                    return True
            else:
                return False
        else:
            if math.isinf(new_dv.cost) or self.id in new_dv.path:
                return False

            self.neighbor_dvs[frozenset(key)] = new_dv
            return True

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        if self.id == 1 and destination == 4:
            print(" ")
        if frozenset((self.id, destination)) in self.my_dvs:
            if self.my_dvs[frozenset((self.id, destination))].cost < float('inf'):
                return self.my_dvs[frozenset((self.id, destination))].path[1]

        return -1
