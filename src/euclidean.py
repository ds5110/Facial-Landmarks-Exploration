import numpy as np
import pandas as pd
import sys
from sklearn.metrics.pairwise import euclidean_distances
from utils import get_data, get_data_scale, get_cols, get_cols_scale, reshape_to_2d


# Calculate Eucidean Distances based on the reshaped 3d DataFrame
# Result would be stored as a (row, 68, 68) DataFrame
def distance_by_coordinates(df, x_cols, y_cols):
    df_reshaped = reshape_to_2d(df, x_cols, y_cols)
    num_rows = df.shape[0]
    distances = np.zeros((num_rows, 68, 68))
    for row in range(num_rows):
        distances[row] = euclidean_distances([coordinates for coordinates in df_reshaped[row]])
    return distances


# Extract the Euclidean Distance data from the result of `distance_by_coordinates`
# Store as a 2d DataFrame
def get_distance_cols(distances):
    new_cols = []
    for i in range(68):
        for j in range(i + 1, 68):
            col_name = f'dist_{i}_{j}'
            new_col = pd.DataFrame({col_name: distances[:, i, j]})
            new_cols.append(new_col)
    new_cols_df = pd.concat(new_cols, axis=1).reset_index(drop=True)
    return new_cols_df


# Combine results of `get_distance_cols` and the original DataFrame together
def create_euclidean_df(df, x_cols, y_cols):
    distances = distance_by_coordinates(df, x_cols, y_cols)
    new_cols_df = get_distance_cols(distances)
    df = df.reset_index(drop=True)
    euclidean_df = pd.concat([df, new_cols_df], axis=1)
    return euclidean_df


def main():
    # Create euclidean distances for merged landmarks
    df = get_data("outcome/prev/merged_landmarks.csv")
    x_cols, y_cols = get_cols(df)
    euclidean_df = create_euclidean_df(df, x_cols, y_cols)

    address = "outcome/euclidean/euclidean_merged.csv"
    euclidean_df.to_csv(address, index=False)
    print("Euclidean distances of merged landmarks have been saved as '{}'.".format(address))


def main_scale():
    # Create euclidean distances for landmarks using scale method
    df = get_data_scale("outcome/scale/rotated_scale.csv")
    x_cols, y_cols = get_cols_scale(df)
    euclidean_df = create_euclidean_df(df, x_cols, y_cols)

    address = "outcome/euclidean/euclidean_merged_scale.csv"
    euclidean_df.to_csv(address, index=False)
    print("Euclidean distances of merged landmarks using scale method have been saved as '{}'.".format(address))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scale":
        main_scale()
    else:
        main()