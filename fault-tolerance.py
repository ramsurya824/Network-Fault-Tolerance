import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import itertools

'''
Algorithm:
Assumption - Single Application Server and multiple Storage Servers
    1. For each combination of routers:
        Remove that combination from the network.
        Then find if a path exists (using BFS) between the AS and all SS. 
    The size of the largest combination that doesn't fail in the connectivity test, is the maximum number of nodes that can fail for the network to be still functional.
    2. Similarly for edges, take all combinations of edges and repeat the same steps as for routers.
    3. Minimum nodes required = Total nodes - Max nodes that can fail (will include storage servers and application server)
    4. Minumum edges required = Total edges - Max edges that can fail 
    5. Remove each router node and if path doesn't exists between the AS and any SS then it is a critical node. Do the same for edges.
'''


def fault_tolerance(G):
    routers = []
    for node, attr in G.nodes(data=True):
        if attr["type"]=="Router":
            routers.append(node)
    for i in range(1, len(routers) + 1):                        
        for nodes_subset in itertools.combinations(routers, i):     
            if simulate_failures(G, list(nodes_subset), []):
                max_node_failures = i
                break
    
    for i in range(1, len(G.edges()) + 1):
        for edges_subset in itertools.combinations(G.edges(), i):
            if simulate_failures(G, [], list(edges_subset)):
                max_edge_failures = i
                break
    
    min_node_required = len(G.nodes()) - max_node_failures
    min_edge_required = len(G.edges()) - max_edge_failures
    
    return max_node_failures, max_edge_failures, min_node_required, min_edge_required

def simulate_failures(G, failed_nodes, failed_edges):
    G_copy = G.copy()
    if len(failed_nodes)>0:
        G_copy.remove_nodes_from(failed_nodes)
    if len(failed_edges)>0:
        G_copy.remove_edges_from(failed_edges)
    return check_connectivity(G_copy)



def critical_nodes_edges(G):
    critical_nodes = []
    critical_edges = []
    
    for node in G.nodes():
        G_copy = G.copy()
        if G.nodes[node]["type"]=="Router":
            G_copy.remove_node(node)
            if not check_connectivity(G_copy):
                critical_nodes.append(node)
    
    for edge in G.edges():
        G_copy = G.copy()
        G_copy.remove_edge(edge[0], edge[1])
        if not check_connectivity(G_copy):
            critical_edges.append((edge))
    
    return critical_nodes, critical_edges



def check_connectivity(G):
    ss = []
    d = None
    for node, attr in G.nodes(data=True):
        if attr["type"]=="Storage Server":
            ss.append(node)
        if attr["type"]=="Application Server":
            d = node

    def bfs(node, d):
        visited  = {}
        q = deque()
        q.append(node)
        visited[node] = True

        while len(q)!=0:
            n = q.popleft()
            if n==d:
                return True
            adj = G[n]
            for i in adj:
                if visited.get(i, False)==False and G.nodes[i]["type"]!="Storage Server":
                    q.append(i)
                    visited[i] = True
        return False
    results = []
    for i in ss:
        results.append(bfs(i, d))
    result = all(results)
    return result 







G = nx.Graph()

# Add nodes

nodes = [
    ("AS", {"type": "Application Server"}),
    ("SS1", {"type": "Storage Server"}),
    ("SS2", {"type": "Storage Server"}),
    ("SS3", {"type": "Storage Server"}),
    ("SS4", {"type": "Storage Server"}),
    ("R1", {"type": "Router"}),
    ("R2", {"type": "Router"}),
    ("R3", {"type": "Router"}),
    ("R4", {"type": "Router"}),
    ("R5", {"type": "Router"})
]
G.add_nodes_from(nodes)

# Add edges
edges = [
    ("SS1", "R1"), ("R1", "R2"), ("R2", "R5"), ("R5", "AS"),
    ("SS2", "R1"), ("SS2", "R2"), ("SS3", "R2"), ("SS3", "R3"),
    ("R3", "R4"), ("R4", "R5"), ("SS4", "R4")
]
G.add_edges_from(edges)

print("Enter\n1. Remove 1 or more nodes\n2. Remove 1 or more edges\n3. Check the fault tolerance of the network\n4. Get critical nodes and edges of the network\n>>")
n = int(input())
if n==1:
    print("Enter the nodes that failed: ")
    nodes = list(map(str, input().split()))
    G.remove_nodes_from(nodes)
    print(f"Connection status: {check_connectivity(G)}")
    if check_connectivity(G):
        a, b, c, d = fault_tolerance(G)
        print(f"Maximum nodes that can fail: {a}")
        print(f"Maximum edges that can fail: {b}")
        print(f"Minimum nodes required: {c}")
        print(f"Minimum edges required: {d}")

        crit_nodes, crit_edges = critical_nodes_edges(G)
        print(f"Critical nodes: {crit_nodes}\nCritical edges: {crit_edges}")
    
elif n==2:
    final_list = [] 
    line = input("Enter the list of tuples:\n") 
    while(line != ''):
        final_list.append(tuple(line.split()))
        line = input()
    print(final_list) 
    G.remove_edges_from(final_list)
    print(f"Connection status: {check_connectivity(G)}")
    if check_connectivity(G):
        a, b, c, d = fault_tolerance(G)
        print(f"Maximum nodes that can fail: {a}")
        print(f"Maximum edges that can fail: {b}")
        print(f"Minimum nodes required: {c}")
        print(f"Minimum edges required: {d}")

        crit_nodes, crit_edges = critical_nodes_edges(G)
        print(f"Critical nodes: {crit_nodes}\nCritical edges: {crit_edges}")
    
elif n==3:
    a, b, c, d = fault_tolerance(G)
    print(f"Maximum nodes that can fail: {a}")
    print(f"Maximum edges that can fail: {b}")
    print(f"Minimum nodes required: {c}")
    print(f"Minimum edges required: {d}")

    

elif n==4:
    crit_nodes, crit_edges = critical_nodes_edges(G)
    print(f"Critical nodes: {crit_nodes}\nCritical edges: {crit_edges}")


else:
    print("Enter a valid option")
