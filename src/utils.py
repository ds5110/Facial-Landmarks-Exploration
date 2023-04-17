import numpy as np
import pandas as pd

# Some common functions that are used by various scripts

# Reshape data frame into a 3d array
# Data in the 3rd dimension would be (x, y) coordinates
def reshape_to_2d(df, x_cols, y_cols):
    df_x_coords = df[x_cols]
    df_y_coords = df[y_cols]
    num_rows = df.shape[0]
    df_reshaped = np.zeros((num_rows, 68, 2))
    df_reshaped[:, :, 0] = df_x_coords
    df_reshaped[:, :, 1] = df_y_coords
    return df_reshaped


# Read CSV file from the pevious program
# Typecast several columns to uniform formats
def get_data(data):
    df = pd.read_csv(data, dtype={
        'image-set': str,
        'filename': str,
        'partition': str,
        'subpartition': str})
    return df


# Read CSV file from scale method part
# Select data from `normalized` method
# Typecast several columns to uniform formats
def get_data_scale(data):
    df = pd.read_csv(data, dtype={
        'image-name': str,
        'scale_type': str})
    df = df.loc[df["scale_type"] == "normalized"]
    return df


# Get x and y coordinates column name lists in the CSV file of the previous program 
def get_cols(df):
    x_cols = [col for col in df.columns if 'norm_cenrot-x' in col]
    y_cols = [col for col in df.columns if 'norm_cenrot-y' in col]
    return x_cols, y_cols


# Get x and y coordinates column name lists in the CSV file from scale method part
def get_cols_scale(df):
    x_cols = [col for col in df.columns if col.startswith("x")]
    y_cols = [col for col in df.columns if col.startswith("y")]
    return x_cols, y_cols
