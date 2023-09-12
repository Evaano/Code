import numpy as np
import math

class simple_KNN:
    def __init__(self, K=1, verbose=False):
        self.distance = self.euclidean_distance
        self.K = K
        self.verbose = verbose

    def fit(self, X, y):
        self.modelX = X
        self.modelY = y
        self.labelsPresent = np.unique(self.modelY)
        if self.verbose:
            print(f"Number of training examples: {len(self.modelX)}")
            print(f"Number of features: {self.modelX.shape[1]}")
            print(f"Labels present: {self.labelsPresent}")

    def predict(self, newItems):
        numToPredict = newItems.shape[0]
        predictions = np.empty(numToPredict)
        for item in range(numToPredict):
            thisPrediction = self.predict_new_item(newItems[item])
            predictions[item] = thisPrediction
        return predictions
    
    def predict_new_item(self, newItem):
        distFromNewItem = np.zeros((len(self.modelX)))
        
        for stored_example in range(len(self.modelX)):
            distFromNewItem[stored_example] = self.distance(newItem, self.modelX[stored_example])

        closestK = self.get_ids_of_k_closest(distFromNewItem, self.K)

        labelcounts = np.zeros(len(self.labelsPresent))
        for k in range(self.K):
            thisindex = closestK[k]
            thislabel = self.modelY[thisindex]
            labelcounts[thislabel] += 1
        thisPrediction = np.argmax(labelcounts)
        return thisPrediction
        
    def euclidean_distance(self, item1, item2):
        assert item1.shape[0] == item2.shape[0]
        distance = 0.0
        for feature in range(item1.shape[0]):
            difference = item1[feature] - item2[feature]
            distance = distance + difference * difference
        return math.sqrt(distance)
    
    def get_ids_of_k_closest(self, distFromNewItem, K):
        sorted_indices = np.argsort(distFromNewItem)
        closestK = sorted_indices[:K]
        return closestK