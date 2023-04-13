import numpy as np
import pandas as pd


def get_infant_cols(infant):
    infant_cols = [col for col in infant.columns if 'gt-' in col]
    infant_x_cols = [col for col in infant.columns if 'gt-x' in col]
    infant_y_cols = [col for col in infant.columns if 'gt-y' in col]
    return infant_cols, infant_x_cols, infant_y_cols


def get_adult_cols(adult):
    adult_cols = [col for col in adult.columns if 'original' in col]
    adult_x_cols = [col for col in adult.columns if 'x' in col]
    adult_y_cols = [col for col in adult.columns if 'y' in col]
    return adult_cols, adult_x_cols, adult_y_cols


# reshape the dataframe to 3d array.
def reshape_to_2d(df1, x_cols, y_cols):
    df1_x_coords = df1[x_cols]
    df1_y_coords = df1[y_cols]
    num_rows = df1_x_coords.shape[0]
    df1_reshaped = np.zeros((num_rows, 68, 2))
    df1_reshaped[:, :, 0] = df1_x_coords
    df1_reshaped[:, :, 1] = df1_y_coords
    return df1_reshaped


def get_data(data):
    df = pd.read_csv(data, dtype={
        'image-set': str,
        'filename': str,
        'partition': str,
        'subpartition': str, })
    return df
