import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def cluster_and_visualise(datafilename, K, featurenames):
    # Read in the dataset from the file
    data = np.genfromtxt(datafilename, delimiter=',')
    fruit_labels = np.genfromtxt('fruit_labels.csv', dtype=str)
    fruit_label_ids = np.genfromtxt('fruit_label_ids.csv', dtype=int)

    # Run the kmeans algorithm
    kmeans = KMeans(n_clusters=K, n_init=10)
    cluster_labels = kmeans.fit_predict(data)

    # Map cluster numbers to fruit names
    cluster_to_fruit = {}
    for i in range(K):
        cluster_data = data[cluster_labels == i]
        cluster_fruit_labels = fruit_labels[fruit_label_ids == i]
        cluster_fruit_name = cluster_fruit_labels[0]
        cluster_to_fruit[i] = cluster_fruit_name

    # Make a 2D visualisation
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Add more colors as needed

    for i in range(K):
        cluster_data = data[cluster_labels == i]
        cluster_fruit_name = cluster_to_fruit[i]
        ax.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'{cluster_fruit_name}', c=colors[i], alpha=0.6)

    # Set titles and labels
    ax.set_title(f'Frooty Patooty - {K} Clusters')
    ax.set_xlabel(featurenames[0])
    ax.set_ylabel(featurenames[1])
    ax.legend()

    # Save the visualisation to a file
    plt.savefig('myVisualisation.jpg')

    # Return the figure and axis
    return fig, ax


if __name__ == "__main__":
    datafilename = 'fruit_values.csv'
    K = 3
    featurenames = ['Um idk like Feature 1', 'Um idk like Feature 2']

    fig, ax = cluster_and_visualise(datafilename, K, featurenames)
    plt.show()
