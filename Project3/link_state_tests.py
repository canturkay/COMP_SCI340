import datetime

from link_state_node import Link_State_Node, Link_State_Edge

node = Link_State_Node(id=1)

link1 = Link_State_Edge()
link1.init(cost=1, time=10)
link2 = Link_State_Edge()
link2.init(cost=2, time=10)
link3 = Link_State_Edge()
link3.init(cost=11, time=10)
link4 = Link_State_Edge()
link4.init(cost=5, time=10)
link5 = Link_State_Edge()
link5.init(cost=1, time=10)
link6 = Link_State_Edge()
link6.init(cost=3, time=10)
link7 = Link_State_Edge()
link7.init(cost=3, time=10)
link8 = Link_State_Edge()
link8.init(cost=2, time=10)
link9 = Link_State_Edge()
link9.init(cost=9, time=10)

link10 = Link_State_Edge()
link10.init(cost=2, time=10)
link11 = Link_State_Edge()
link11.init(cost=8, time=10)


link12 = Link_State_Edge()
link12.init(cost=10, time=10)
link13 = Link_State_Edge()
link13.init(cost=20, time=10)
link14 = Link_State_Edge()
link14.init(cost=18, time=10)


node.process_incoming_routing_message(
    m = "{"
        "\"(2,1)\": " + str(link1) +
        ",\"(1,3)\": " + str(link2) +
        ",\"(6,1)\": " + str(link3) +
        ",\"(2,4)\": " + str(link4) +
        ",\"(2,5)\": " + str(link5) +
        ",\"(3,5)\": " + str(link6) +
        ",\"(4,6)\": " + str(link7) +
        ",\"(4,5)\": " + str(link8) +
        ",\"(5,6)\": " + str(link9) +
        ",\"(6,7)\": " + str(link10) +
        ",\"(5,7)\": " + str(link11) +
        ",\"(7,8)\": " + str(link12) +
        ",\"(8,5)\": " + str(link13) +
        ",\"(3,8)\": " + str(link14) +
        "}"
)

print(node.edges)
print(node.dijkstra(destination=8))

node.link_has_been_updated(neighbor=2, latency=-1)
print(node.edges)
print(node.dijkstra(destination=8))

link1.cost = 0
link1.time = 10
link6.cost = 2
link7.cost = 0
link7.time = 11
node.process_incoming_routing_message(
    m = "{"
        "\"(2,1)\": " + str(link1) +
        ",\"(1,3)\": " + str(link2) +
        ",\"(6,1)\": " + str(link3) +
        ",\"(2,4)\": " + str(link4) +
        ",\"(2,5)\": " + str(link5) +
        ",\"(5,3)\": " + str(link6) +
        ",\"(6,4)\": " + str(link7) +
        ",\"(4,5)\": " + str(link8) +
        ",\"(5,6)\": " + str(link9) +
        ",\"(6,7)\": " + str(link10) +
        ",\"(5,7)\": " + str(link11) +
        ",\"(7,8)\": " + str(link12) +
        ",\"(8,5)\": " + str(link13) +
        ",\"(3,8)\": " + str(link14) +
        "}"
)
print(node.edges)
print(node.dijkstra(destination=8))
