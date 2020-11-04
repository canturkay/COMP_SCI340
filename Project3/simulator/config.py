from generic_node import Generic_Node
from distance_vector_node import Distance_Vector_Node
from link_state_node import Link_State_Node

ROUTE_ALGORITHM = [
    "GENERIC",
    "DISTANCE_VECTOR",
    "LINK_STATE"
]

STEP_COMMAND = [
    "NORMAL",
    "SINGLE_STEP",
    "NO_STOP"
]

ROUTE_ALGORITHM_NODE = {
    "GENERIC" : Generic_Node,
    "DISTANCE_VECTOR" : Distance_Vector_Node,
    "LINK_STATE" : Link_State_Node
}

class EVENT_TYPE:
    ADD_NODE = "ADD_NODE"
    ADD_LINK = "ADD_LINK"

    DELETE_NODE = "DELETE_NODE"
    DELETE_LINK = "DELETE_LINK"

    CHANGE_LINK = "CHANGE_LINK"

    PRINT = "PRINT"
    DRAW_TOPOLOGY = "DRAW_TOPOLOGY"
    DRAW_PATH = "DRAW_PATH"
    DRAW_TREE = "DRAW_TREE"
    DUMP_NODE = "DUMP_NODE"
    DUMP_SIM = "DUMP_SIM"

    # Not for user
    ROUTING_MESSAGE_ARRIVAL = "ROUTING_MESSAGE_ARRIVAL"
    SEND_LINK = "SEND_LINK"


OUTPUT_PATH = "output/"

USAGE_STR = "usage: sim.py route_algorithm event [step=NORMAL]\n" \
            "\troute_algorithm\t- {GENERIC DISTANCE_VECTOR LINK_STATE}\n" \
            "\tevent\t\t\t- a file\n" \
            "\tstep\t\t\t- {NORMAL SINGLE_STEP NO_STOP}"


LOGGING_FORMAT = "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"

LOGGING_DATAFMT = '%Y-%m-%d %H:%M:%S'
