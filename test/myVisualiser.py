import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def cluster_and_visualise(datafilename, K, featurenames):
    data = np.genfromtxt(datafilename, delimiter=',')

    if K > len(featurenames):
        raise ValueError("Number of clusters (K) must be less than or equal to the number of features.")

    kmeans = KMeans(n_clusters=K)
    cluster_labels = kmeans.fit_predict(data)
    cluster_centers = kmeans.cluster_centers_

    num_features = len(featurenames)
    fig, axs = plt.subplots(num_features, num_features, figsize=(12, 12))

    # Calculate histograms for each feature in data
    histograms = [np.histogram(data[:, i], bins='auto') for i in range(num_features)]

    # Define different colors for the clusters
    cluster_colors = ['blue', 'orange', 'green', 'purple', 'cyan', 'magenta', 'yellow', 'pink']

    # Visualize scatter plots for different combinations of features
    for i in range(num_features):
        for j in range(num_features):
            ax = axs[j, i]  # Corrected indexing
            if i == j:
                # Plot histograms for variables on diagonals
                for cluster_num in range(K):
                    ax.hist(data[cluster_labels == cluster_num, i], bins=histograms[i][1], alpha=0.5,
                            color=cluster_colors[cluster_num % len(cluster_colors)], label=f'Cluster {cluster_num + 1}')

            else:
                # Scatter plots for different combinations of features
                for cluster_num in range(K):
                    ax.scatter(data[cluster_labels == cluster_num, i], data[cluster_labels == cluster_num, j],
                               label=f'Cluster {cluster_num + 1}', alpha=0.5, color=cluster_colors[cluster_num % len(cluster_colors)])
                ax.scatter(cluster_centers[:, i], cluster_centers[:, j], c='red', marker='x', s=100,
                           label='Cluster Centers')

            ax.set_xlabel(featurenames[i])
            ax.set_ylabel(featurenames[j])
    ax.legend(loc='upper left')  # Place legend in upper left

    plt.subplots_adjust(hspace=0.4, wspace=0.5)
    fig.suptitle(f'K-Means Clustering by {",".join(featurenames)} - K={K} Made by ei2-rasheed', fontsize=15)
    fig.text(0.6, 0.01, 'Made by ei2-rasheed', ha='right', va='bottom')
    plt.savefig('myVisualisation.jpg')
    plt.show()

    return fig, axs