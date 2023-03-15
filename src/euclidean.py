import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import utils

standard_infant = pd.read_csv('./outcome/scale/standard_infant.csv')
standard_adult = pd.read_csv('./outcome/scale/standard_adult.csv')


def euclidean_distance_by_coordinates(df, x_cols, y_cols):
    df_reshaped = utils.reshape_to_2d(df, x_cols, y_cols)
    num_rows = df[x_cols].shape[0]
    distances = np.zeros((num_rows, 68, 68))
    for row in range(num_rows):
        distances[row] = euclidean_distances([coordinates for coordinates in df_reshaped[row]])
    return distances

def euclidean_distance():
    euclidean_infant = standard_infant.copy()
    infant_cols, infant_x_cols, infant_y_cols = utils.get_infant_cols(standard_infant)
    infant_distances = euclidean_distance_by_coordinates(standard_infant, infant_x_cols, infant_y_cols)
    for i in range(68):
        for j in range(i + 1, 68):
            euclidean_infant[f'dist_{i}_{j}'] = infant_distances[:, i, j]
    euclidean_infant.to_csv('./outcome/euclidean/euclidean_infant.csv', index=False)

    euclidean_adult = standard_adult.copy()
    adult_cols, adult_x_cols, adult_y_cols = utils.get_adult_cols(standard_adult)
    adult_distances = euclidean_distance_by_coordinates(standard_adult, adult_x_cols, adult_y_cols)
    for i in range(68):
        for j in range(i + 1, 68):
            euclidean_adult[f'dist_{i}_{j}'] = adult_distances[:, i, j]
    euclidean_adult.to_csv('./outcome/euclidean/euclidean_adult.csv', index=False)


euclidean_distance()