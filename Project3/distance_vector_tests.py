from distance_vector_node import Distance_Vector, Distance_Vector_Node

node = Distance_Vector_Node(id=1)

dv1 = Distance_Vector(cost=3, path=[2, 1], time=10)
dv2 = Distance_Vector(cost=12, path=[3, 2, 1], time=10)
dv3 = Distance_Vector(cost=9, path=[3, 2], time=10)
dv4 = Distance_Vector(cost=9, path=[2, 3], time=10)
dv5 = Distance_Vector(cost=15, path=[3, 4], time=10)
dv6 = Distance_Vector(cost=16, path=[3, 4, 5], time=10)
dv7 = Distance_Vector(cost=14, path=[2, 3, 4], time=10)
dv8 = Distance_Vector(cost=25, path=[2, 3, 4, 5], time=10)

dv9 = Distance_Vector(cost=0, path=[2], time=10)
dv10 = Distance_Vector(cost=0, path=[3], time=10)

node.link_has_been_updated(neighbor=2, latency=3)
node.link_has_been_updated(neighbor=3, latency=20)

node.process_incoming_routing_message(m="{"
                                        "\"(2,1)\": " + str(dv1) +
                                        ",\"(3,1)\": " + str(dv2) +
                                        ",\"(2,3)\": " + str(dv3) +
                                        ",\"(2,4)\": " + str(dv7) +
                                        ",\"(2,5)\": " + str(dv8) +
                                        ",\"(2,2)\": " + str(dv9) +
                                        "}")

node.process_incoming_routing_message(m="{"
                                        "\"(2,3)\": " + str(dv4) +
                                        ",\"(3,4)\": " + str(dv5) +
                                        ",\"(3,5)\": " + str(dv6) +
                                        ",\"(3,3)\": " + str(dv10) +
                                        "}")

print(node.get_next_hop(destination=2))
print(node.get_next_hop(destination=3))
print(node.get_next_hop(destination=4))
print(node.get_next_hop(destination=5))

node.link_has_been_updated(neighbor=2, latency=100)

print(node.get_next_hop(destination=2))
print(node.get_next_hop(destination=3))
print(node.get_next_hop(destination=4))
print(node.get_next_hop(destination=5))