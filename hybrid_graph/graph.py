from itertools import chain
import networkx as nx
from networkx.generators.random_graphs import _random_subset


def simple_hybrid_graph(t, m=2, alpha=0.5):
    """Generates a random graph that uses a mixed model for growth. 
       For each unit of time t, a new node links to the graph with 
       m * alpha links assigned randomly to existing nodes, and 
       m * (1 - alpha) links assigned to neighbors of the above random nodes.
       alpha near 1 produces a nearly exponential degree distribution, 
       alpha near 0 produces a nearly preferential (scale free) 
       degree distribution.
       IMPORTANT: m % alpha == 0"""
    beta = 1 - alpha
    random = int(alpha * m)
    preferential = int(beta * m)
    G = nx.empty_graph(random)
    targets = list(range(random))
    source = random
    while source < t:
        G.add_edges_from(zip([source] * random, targets))
        neighbors = chain.from_iterable([G.neighbors(node) 
                                         for node in targets])
        neighbors = filter(lambda x: x != source, neighbors)
        # Grows randomly with alpha * m # of links until there is a
        # neighbor, then adds all neighbors until len of neighbors is
        # greater than # of preferential neighbors to be added. After
        # random selection, preferential attachment of neighbors begins 
        # normally.
        if len(neighbors) > preferential:
            neighbor_targets = _random_subset(neighbors, preferential)
            G.add_edges_from(zip([source] * preferential, neighbor_targets))
        elif len(neighbors) > 0:
             G.add_edges_from(zip([source] * len(neighbors), neighbors))
        # Select new targets.
        targets = _random_subset(G.nodes(), random)
        source += 1
    return G