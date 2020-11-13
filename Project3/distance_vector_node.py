import copy
import json
import math

from simulator.node import Node


class Distance_Vector:
    def __init__(self, cost: int, path: list):
        self.cost = cost
        self.path = path

    def is_newer_than(self, other: int):
        return self.time > other

    def from_str(self, message: str):
        json_value = json.loads(message)
        self.from_map(json_value)

    def from_map(self, json_value):
        self.cost = int(json_value["cost"])
        self.path = int(json_value["path"])

    def __str__(self):
        return json.dumps(
            self.as_dict()
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.cost == other.cost and self.path == other.path

    def as_dict(self):
        return {
            "cost": self.cost,
            "path": self.path
        }


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.my_dvs = {}
        self.neighbor_dvs = {}
        self.dv_seqnum = {}
        self.link_costs = {}
        self.seq_num = 0

    def __str__(self):
        message = {}
        for dst, val in self.my_dvs.items():
            message[dst] = val.as_dict()

        message[-1] = self.seq_num
        self.seq_num += 1

        return copy.deepcopy(json.dumps(message))

    def link_has_been_updated(self, neighbor, latency):
        if latency == -1:
            del self.link_costs[neighbor]
            del self.neighbor_dvs[neighbor]

        else:
            self.link_costs[neighbor] = (latency, self.get_time())

        self.recompute_dvs()
        pass

    def recompute_dvs(self):
        old_dvs = copy.deepcopy(self.my_dvs)
        self.my_dvs = {}

        for neighbor, link_cost in self.link_costs.items():
            self.my_dvs[neighbor] = Distance_Vector(cost=link_cost[0], path=[self.id, neighbor])

        # for neighbor, value in self.link_costs.items():
        #     cost = value[0]
        #     time = value[1]
        #
        #     self.my_dvs[frozenset((self.id, neighbor))] = Distance_Vector_Edge(cost=cost, path=[self.id, neighbor],
        #                                                                        time=time)
        for source, dvs in self.neighbor_dvs.items():
            for destination, dv in dvs.items():
                self.recompute_single_dv(src=source, dst=destination, dv=dv)

        if self.my_dvs != old_dvs:
            self.broadcast_to_neighbors()

    def recompute_single_dv(self, src: int, dst: int, dv: Distance_Vector):
        new_cost = dv.cost + self.link_costs[src][0]
        if dst not in self.my_dvs or (dst in self.my_dvs and new_cost < self.my_dvs[dst].cost):
            new_path = [self.id] + copy.deepcopy(dv.path)
            self.my_dvs[dst] = Distance_Vector(cost=new_cost, path=new_path)

    def broadcast_to_neighbors(self):
        self.send_to_neighbors(str(self))
        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        _neighbor_dvs = json.loads(m)

        seq_num = _neighbor_dvs['-1']
        del _neighbor_dvs['-1']

        changed = False

        # time_sent = _neighbor_dvs['time_sent']
        # del _neighbor_dvs['time_sent']

        neighbor = int(_neighbor_dvs[next(iter(_neighbor_dvs))]['path'][0])

        to_delete = []

        self.dv_seqnum[neighbor] = seq_num

        if neighbor not in self.neighbor_dvs:
            self.neighbor_dvs[neighbor] = {}

        for dst, value in copy.deepcopy(self.neighbor_dvs[neighbor]).items():
            to_delete.append(dst)

        for dst_str, value in _neighbor_dvs.items():
            dst = int(dst_str)
            if dst in to_delete:
                to_delete.remove(dst)

            link = Distance_Vector(cost=value['cost'], path=value['path'])

            changed = self.process_neighbor_dv(src=neighbor, dst=dst, dv=link, seq_num=seq_num) or changed

        for dst in to_delete:
            del self.neighbor_dvs[neighbor][dst]
            changed = True

        if changed:
            self.recompute_dvs()

    def process_neighbor_dv(self, src: int, dst: int, dv: Distance_Vector, seq_num: int):
        if dst in self.neighbor_dvs[src]:
            if self.id in dv.path:
                del self.neighbor_dvs[src][dst]
                return True

            if seq_num > self.dv_seqnum[src]:
                self.neighbor_dvs[src][dst] = dv
                return True
            return False
        else:
            if self.id in dv.path:
                return False
            else:
                self.neighbor_dvs[src][dst] = dv
                return True

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        # if self.id == 1 and destination == 4:
        #     print(" ")
        if destination in self.my_dvs:
            if self.my_dvs[destination].cost < float('inf'):
                return copy.deepcopy(self.my_dvs[destination].path)[1]

        return -1
