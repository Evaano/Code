import numpy as np
import pandas as pd

def cluster_and_visualise(datafilename, K, featurenames):
    data = pd.read_csv('data.csv')