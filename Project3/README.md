# Routesim2

This is a simple network routing simulator written in Python.  It was primarily written by Kaiyu Hou, with minor tweaks by Steve Tarzia.  This code is based on the C++ Routesim code written by Peter Dinda.

This code is the basis for a programming project for Northwestern's University's EECS-340 Introduction to Computer Networking.

### Prerequisites:

This code is written for Python 3 and it was tested on version 3.5.  Run the following to install the two required packages:

    $ pip install --user networkx matplotlib

### Running:

    $ python3 sim.py GENERIC demo.event
    
The first parameter can be either GENERIC, LINK_STATE, or DISTANCE_VECTOR.  The second parameter specifies the input file.

### Running on Murphy:

For CS-340, if you choose to run your code on the old murphy.wot.eecs.northwestern.edu machine then you can run the following commands to use Python 3.5.  However, a better choice would be using the newer machine moore.wot.eecs.northwestern.edu.

    $ scl enable rh-python35 bash
    $ pip install --user matplotlib networkx
    $ python3 sim.py GENERIC demo.event 
    
### Functions provide in Node class
    0. send_to_neighbors(m)  // send message to neighbors
    1. send_to_neighbor(neighbor, m) // send message to a neighbor
    2. get_time()  // get current simulator time
    3. link_has_been_updated() // will be called by simulator after processing every event in that second.

### Event commands:
     0. # [comment]
        e.g. # this is a comment

     1. [Time] ADD_NODE [ID], # [ID] is any hashable value
        e.g., 10 ADD_NODE 1
     2. [Time] ADD_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 ADD_LINK 1 2 10
     3. [Time] DELETE_NODE [ID], # [ID] is any hashable value
        e.g., 10 DELETE_NODE 1
     4. [Time] CHANGE_LINK [ID1] [ID2] [LATENCY], # will create a new node if does not exist
        e.g., 10 CHANGE_LINK 1 2 10
     5. [Time] DELETE_LINK [ID1] [ID2], # will send latency -1 to node1 and node 2
        e.g., 10 DELETE_LINK 1 2

     6. [Time] PRINT [Text]
        e.g. 10 PRINT "Debug information"
     7. [Time] DRAW_TOPOLOGY
        e.g. 10 DRAW_TOPOLOGY
     8. [Time] DRAW_PATH [ID1] [ID2]  # Draw shortest path from ID1 to ID2, Green path: correct path, Red path: your path
        e.g. 1000 DRAW_PATH 1 2
     9. [Time] DRAW_TREE [ID] # Draw shortest path tree, take ID as root
        e.g. 1000 DRAW_TREE 1

     10. [Time] DUMP_NODE [ID]
        e.g. 10 DUMP_NODE 1
     11. [Time] DUMP_SIM
        e.g. 1 DUMP_SIM # It will print topology and event stack. For debug purpose.

