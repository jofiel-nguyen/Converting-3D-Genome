import hicstraw
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def get_matrix(hic_file, data_type='observed', chromosome1='1', chromosome2='1', chromosome1_start=0, chromosome1_end=5000000, chromosome2_start=0, chromosome2_end=5000000, resolution=100000, normalization='KR'):
    hic = hicstraw.HiCFile(hic_file)
    mzd = hic.getMatrixZoomData(chromosome1, chromosome2, data_type, normalization, "BP", resolution)
    numpy_matrix = mzd.getRecordsAsMatrix(chromosome1_start, chromosome1_end, chromosome2_start, chromosome2_end)
    return numpy_matrix

def numpy_matrix_to_network_graph(matrix):
    # Ensure the input is a numpy matrix
    if not isinstance(matrix, np.ndarray):
        raise ValueError("Input should be a numpy matrix")

    # Create an empty graph
    graph = nx.Graph()

    # Add edges based on the matrix with weights
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] != 0:
                graph.add_edge(i, j, weight=matrix[i, j])  
    return graph

def plot_network_graph(graph, graph_type='Weighted', method='Original'):
    plt.figure()
    nx.draw(graph, with_labels=True)
    plt.title('{} Graph (Method: {})'.format(graph_type, method))
    plt.show()

def plot_histogram(edge_weights):
    plt.hist(edge_weights, bins=20)  
    plt.xlabel('Edge Weight')
    plt.ylabel('Frequency')
    plt.title('Histogram of Edge Weights')
    plt.show()

def threshold_network(graph, threshold):
    # Create a copy of the original graph
    thresholded_graph = graph.copy()
    
    # Iterate through edges and remove edges below the threshold
    for u, v, data in graph.edges(data=True):
        if data.get('weight', 1) < threshold:  # Default weight to 1 if no weight attribute is found
            thresholded_graph.remove_edge(u, v)
    
    return thresholded_graph

def calculate_threshold(edge_weights, method='percentage', threshold_value=None, percentage=None, alpha=None):
  if method == 'value':
    if threshold_value is None:
      raise ValueError("Threshold value must be provided.")
    return threshold_value
  elif method == 'percentage':
    if percentage is None:
      raise ValueError("Percentage must be provided.")
    max_weight = max(edge_weights)
    threshold = max_weight * percentage
    return threshold
  elif method == 'percolation':
    if alpha is None:
      raise ValueError("Alpha value must be provided for percolation method.")
    # Calculate the number of nodes (assuming n0 is the total number of nodes)
    n0 = len(graph.nodes())  # Assuming graph is the network graph object
    threshold = alpha * n0  # Implement percolation threshold formula
    return threshold
  else:
    raise ValueError("Invalid method. Please choose 'value', 'percentage', or 'percolation'.")

# Load hic file
hic_file_path = '' 
x = get_matrix(hic_file_path)

# Convert matrix to network graph
graph = numpy_matrix_to_network_graph(x)

# Extract edge weights for histogram
edge_weights = [data['weight'] for u, v, data in graph.edges(data=True)]

# Plot histogram of edge weights
plot_histogram(edge_weights)

# Choose the method for threshold calculation ('value' or 'percentage')
method = 'percentage'  

# Calculate threshold based on the chosen method
threshold_value = calculate_threshold(edge_weights, method=method, percentage=0.5)

# Thresholding
thresholded_graph = threshold_network(graph, threshold_value)

# Plot the thresholded unweighted graph
plot_network_graph(thresholded_graph, graph_type='Unweighted', method='Thresholded')


