import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import word_frequency_calculator


def create_word_graph(speeches):
    """
    Create the word graph from param: speeches
    return the graph
    """
    G = nx.Graph()

    for speech in speeches:
        words = speech.split()
        G.add_nodes_from(words) #making nodes

        # Connect each word to its 10 neighbors (5 before and 5 after)
        for word in words:
            # List of neighbors for current word
            neighbors = words[max(0, words.index(word) - 5):words.index(word)] + words[words.index(word) + 1:words.index(word) + 6]
            
            G.add_edges_from(combinations([word] + neighbors, 2)) # Edges from combination of all pairs  
    G.remove_edges_from(nx.selfloop_edges(G)) # remove cycling references 
    return G

def plot_word_graph(graph):
    """
    Plot the graph
    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_size=4, node_size=20, font_color='black')
    plt.show()

def k_core_decomposition(graph):
    """
    k-Decompose graph
    """
    k_cores = nx.k_core(graph, k=50)
    return k_cores

def extract_top_words(graph, top_n):
    """
    extract topn words form graph
    """
    degrees = dict(graph.degree())
    #sort nodes based on the degree of each node
    sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    # make list of topk words excluding irrelevant words
    top_words = [word for word, degree in sorted_degrees[:top_n] if word not in word_frequency_calculator.irrelevant_words] 
    return top_words


def getkeywords(speeches):

    print('Creating graph of original data....')
    word_graph = create_word_graph(speeches)

    # print('Plot graph of original data....')
    # plot_word_graph(word_graph) # original speeches graph

    print('Decomposition.....')
    k_core_result = k_core_decomposition(word_graph) # Perform decomposition 

    # print('Plot graph of processed data....')
    # plot_word_graph(k_core_result) # the words after decomposition

    return extract_top_words(k_core_result, top_n=100)
