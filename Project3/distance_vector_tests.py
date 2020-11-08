from distance_vector_node import Distance_Vector_Edge, Distance_Vector_Node

node = Distance_Vector_Node(id=1)

dv1 = Distance_Vector_Edge(cost=3, path=[2,1], time=10)
dv2 = Distance_Vector_Edge(cost=12, path=[3,2,1], time=10)
dv3 = Distance_Vector_Edge(cost=9, path=[3,2], time=10)
dv4 = Distance_Vector_Edge(cost=9, path=[2,3], time=10)
dv5 = Distance_Vector_Edge(cost=15, path=[3,4], time=10)
dv6 = Distance_Vector_Edge(cost=16, path=[3,4,5], time=10)

node.link_has_been_updated(neighbor=2, latency=3)
node.link_has_been_updated(neighbor=3, latency=20)

node.process_incoming_routing_message(m="{"
                                        "\"(2,1)\": " + str(dv1) +
                                        ",\"(3,1)\": " + str(dv2) +
                                        ",\"(2,3)\": " + str(dv3) +
                                        ",\"(2,3)\": " + str(dv4) +
                                        ",\"(3,4)\": " + str(dv5) +
                                        ",\"(3,5)\": " + str(dv6) +
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