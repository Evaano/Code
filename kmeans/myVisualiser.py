import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def cluster_and_visualise(datafilename, K, featurenames):
    data = np.genfromtxt(datafilename, delimiter=',')

    clusterModel = KMeans(n_clusters=K)
    cluster_ids = clusterModel.fit_predict(data)

    f = data.shape[1]

    fig, ax = plt.subplots(f, f, figsize=(12, 12))
    fig.set_size_inches(20, 20)
    fig.patch.set_facecolor('lightgray')

    num_segments = K  # Number of segments equals the number of clusters
    cmap = plt.get_cmap('plasma')  # Use the 'plasma' colormap

    for feature1 in range(f):
        ax[feature1, 0].set_ylabel(featurenames[feature1])
        ax[0, feature1].set_xlabel(featurenames[feature1])
        ax[0, feature1].xaxis.set_label_position('top')

        for feature2 in range(f):
            xdata = data[:, feature1]
            ydata = data[:, feature2]

            if feature1 != feature2:
                ax[feature1, feature2].scatter(xdata, ydata, c=cluster_ids, cmap=cmap, s=10)
            else:
                hist_data = []
                for cluster in range(num_segments):
                    cluster_data = xdata[cluster_ids == cluster]
                    hist_data.append(cluster_data)

                ax[feature1, feature2].hist(hist_data, color=[cmap(i) for i in np.linspace(0, 1, num_segments)], bins=20, alpha=0.7, label=[f"Cluster {cluster + 1}" for cluster in range(num_segments)])
                ax[feature1, feature2].legend()

    fig.suptitle(f"Scatter Plots by {featurenames} of {K} Clusters \nBy ei2-rasheed", fontsize=16, y=0.925, fontweight='semibold')
    fig.subplots_adjust(top=0.85)
    plt.savefig('myVisualisation.png')
    plt.show()

    return fig, ax