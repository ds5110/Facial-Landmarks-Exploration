import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
import utils


def euclidean_distance_by_coordinates(df, x_cols, y_cols):
    df_reshaped = utils.reshape_to_2d(df, x_cols, y_cols)
    num_rows = df[x_cols].shape[0]
    distances = np.zeros((num_rows, 68, 68))
    for row in range(num_rows):
        distances[row] = euclidean_distances([coordinates for coordinates in df_reshaped[row]])
    return distances


def euclidean_distance_to_df(distances):
    new_cols = []
    for i in range(68):
        for j in range(i + 1, 68):
            col_name = f'dist_{i}_{j}'
            new_col = pd.DataFrame({col_name: distances[:, i, j]})
            new_cols.append(new_col)
    return new_cols
    

def main():
    standard_infant = pd.read_csv("outcome/scale/standard_infant.csv")
    standard_adult = pd.read_csv("outcome/scale/standard_adult.csv")

    # Create euclidean distances of infant
    infant_cols, infant_x_cols, infant_y_cols = utils.get_infant_cols(standard_infant)
    infant_distances = euclidean_distance_by_coordinates(standard_infant, infant_x_cols, infant_y_cols)
    new_cols_infant = euclidean_distance_to_df(infant_distances)
    euclidean_df_infant = pd.concat([standard_infant] + new_cols_infant, axis=1)
    euclidean_df_infant.to_csv("outcome/euclidean/euclidean_infant.csv", index=False)

    # Create euclidean distances of adult
    adult_cols, adult_x_cols, adult_y_cols = utils.get_adult_cols(standard_adult)
    adult_distances = euclidean_distance_by_coordinates(standard_adult, adult_x_cols, adult_y_cols)
    new_cols_adult = euclidean_distance_to_df(adult_distances)
    euclidean_df_adult = pd.concat([standard_adult] + new_cols_adult, axis=1)
    euclidean_df_adult.to_csv("outcome/euclidean/euclidean_adult.csv", index=False)

    # Concat results of infant and adult
    num_rows_infant = euclidean_df_infant.shape[0]
    num_rows_adult = euclidean_df_adult.shape[0]
    euclidean_df_infant_image_name = pd.DataFrame({"image_name": euclidean_df_infant["image-set"].str.cat(euclidean_df_infant["filename"], sep="/")})
    euclidean_df_infant_new = pd.concat([euclidean_df_infant_image_name] + new_cols_infant + [pd.DataFrame({"baby": [1] * num_rows_infant}, index=range(num_rows_infant))], axis=1)
    euclidean_df_adult_new = pd.concat([euclidean_df_adult.iloc[:, 0]] + new_cols_adult + [pd.DataFrame({"baby": [0] * num_rows_adult}, index=range(num_rows_adult))], axis=1)
    euclidean_df = pd.concat([euclidean_df_infant_new, euclidean_df_adult_new], axis=0)
    euclidean_df.to_csv("outcome/euclidean/euclidean_all.csv", index=False)


if __name__ == "__main__":
    main()


