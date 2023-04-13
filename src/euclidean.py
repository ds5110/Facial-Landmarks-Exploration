import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from utils import get_data, get_data_scale, get_cols, get_cols_scale, reshape_to_2d


def distance_by_coordinates(df, x_cols, y_cols):
    df_reshaped = reshape_to_2d(df, x_cols, y_cols)
    num_rows = df.shape[0]
    distances = np.zeros((num_rows, 68, 68))
    for row in range(num_rows):
        distances[row] = euclidean_distances([coordinates for coordinates in df_reshaped[row]])
    return distances


def distance_cols(distances):
    new_cols = []
    for i in range(68):
        for j in range(i + 1, 68):
            col_name = f'dist_{i}_{j}'
            new_col = pd.DataFrame({col_name: distances[:, i, j]})
            new_cols.append(new_col)
    new_cols_df = pd.concat(new_cols, axis=1).reset_index(drop=True)
    return new_cols_df
    

# def create_euclidean_df_infant(normalized_infant):
#     infant_cols, infant_x_cols, infant_y_cols = utils.get_infant_cols(normalized_infant)
#     infant_distances = euclidean_distance_by_coordinates(normalized_infant, infant_x_cols, infant_y_cols)
#     new_cols_infant = euclidean_distance_to_df(infant_distances)
#     euclidean_df_infant = pd.concat([normalized_infant] + new_cols_infant, axis=1)
#     return euclidean_df_infant, new_cols_infant


# def create_euclidean_df_adult(normalized_adult):
#     adult_cols, adult_x_cols, adult_y_cols = utils.get_adult_cols(normalized_adult)
#     adult_distances = euclidean_distance_by_coordinates(normalized_adult, adult_x_cols, adult_y_cols)
#     new_cols_adult = euclidean_distance_to_df(adult_distances)
#     euclidean_df_adult = pd.concat([normalized_adult] + new_cols_adult, axis=1)
#     return euclidean_df_adult, new_cols_adult


def create_euclidean_df(df, x_cols, y_cols):
    distances = distance_by_coordinates(df, x_cols, y_cols)
    new_cols_df = distance_cols(distances)
    df = df.reset_index(drop=True)
    euclidean_df = pd.concat([df, new_cols_df], axis=1)
    return euclidean_df


def main():
    # normalized_infant = pd.read_csv("outcome/scale/normalized_infant.csv")
    # normalized_adult = pd.read_csv("outcome/scale/normalized_adult.csv")

    # # Create euclidean distances of infant
    # euclidean_df_infant, new_cols_infant = create_euclidean_df_infant(normalized_infant)
    # address = "outcome/euclidean/euclidean_infant.csv"
    # euclidean_df_infant.to_csv(address, index=False)
    # print("Euclidean distances of infant has been saved as {}.".format(address))

    # # Create euclidean distances of adult
    # euclidean_df_adult, new_cols_adult = create_euclidean_df_adult(normalized_adult)
    # address = "outcome/euclidean/euclidean_adult.csv"
    # euclidean_df_adult.to_csv(address, index=False)
    # print("Euclidean distances of adult has been saved as {}.".format(address))

    # Create euclidean distances for merged landmarks
    df = get_data("outcome/prev/merged_landmarks.csv")
    x_cols, y_cols = get_cols(df)
    euclidean_df = create_euclidean_df(df, x_cols, y_cols)

    address = "outcome/euclidean/euclidean_merged.csv"
    euclidean_df.to_csv(address, index=False)
    print("Euclidean distances of merged landmarks have been saved as '{}'.".format(address))
    

    # Create euclidean distances for landmarks using scale method
    df = get_data_scale("outcome/scale/rotated_scale.csv")
    x_cols, y_cols = get_cols_scale(df)
    euclidean_df = create_euclidean_df(df, x_cols, y_cols)

    address = "outcome/euclidean/euclidean_merged_scale.csv"
    euclidean_df.to_csv(address, index=False)
    print("Euclidean distances of merged landmarks using scale method have been saved as '{}'.".format(address))

if __name__ == "__main__":
    main()


