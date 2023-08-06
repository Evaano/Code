import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

plt.rcParams['font.size'] = 10

def cluster_and_visualise(datafilename, K, featurenames, n_init=30):
    data = np.genfromtxt(datafilename, delimiter=',')

    kmeans = KMeans(n_clusters=K)

    cluster_labels = kmeans.fit_predict(data)

    cluster_centers = kmeans.cluster_centers_
    
    num_features = len(featurenames)

    fig, axs = plt.subplots(num_features, num_features, figsize=(12, 12))

    cluster_colors = ['red', 'blue', 'green', 'pink', 'lightblue']
    histogram_colors = ['pink', 'lightblue', 'pink', 'lightblue', 'pink']
    marker_color = 'black'

    for i, center in enumerate(cluster_centers):
        for j in range(num_features):
            for k in range(num_features):
                if j != k:
                    axs[j, k].scatter(center[j], center[k], s=50, c=marker_color, marker='X')

    # Add a legend for the cluster centers
    handles = []
    for i in range(K):
        handle = axs[num_features - 1, 0].scatter([], [], s=30, c=[cluster_colors[i]], marker='o', label=f'Cluster {i + 1}')
        handles.append(handle)


    title_pos = axs[0, 0].get_position().get_points()
    fig.legend(loc='upper right', bbox_to_anchor=(1, title_pos[1, 1]))


    for i in range(num_features):
        for j in range(num_features):
            if i == j:

                for k in range(K):
                    cluster_data = data[cluster_labels == k]
                    axs[i, j].hist(cluster_data[:, i], bins='auto', color=histogram_colors[k], alpha=0.8)

                axs[i, j].set_xlabel(featurenames[i])
                axs[i, j].set_ylabel(featurenames[j])
            else:

                for k in range(K):
                    cluster_data = data[cluster_labels == k]
                    axs[i, j].scatter(cluster_data[:, i], cluster_data[:, j], alpha=0.5, c=cluster_colors[k], s=10)

                axs[i, j].set_xlabel(featurenames[i])
                axs[i, j].set_ylabel(featurenames[j])

    for i in range(num_features):
        axs[i, 0].set_ylabel(featurenames[i])
        axs[-1, i].set_xlabel(featurenames[i])

    for ax in axs.flat:
        ax.label_outer()
        

    fig.suptitle(f'K-Means Clustering by {",".join(featurenames)} by ei2-rasheed', fontsize=15)
    fig.text(0.99, 0.01, 'Made by ei2-rasheed', ha='right', va='bottom')
    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    plt.savefig("myVisualisation.jpg")

    if num_features == 1:
        return fig, axs[0]
    else:
        return fig, axs
