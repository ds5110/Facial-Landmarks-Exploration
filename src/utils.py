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


def reshape_to_2d(df1, x_cols, y_cols):
    df1_x_coords = df1[x_cols]
    df1_y_coords = df1[y_cols]
    num_rows = df1_x_coords.shape[0]
    df1_reshaped = np.zeros((num_rows, 68, 2))
    df1_reshaped[:, :, 0] = df1_x_coords
    df1_reshaped[:, :, 1] = df1_y_coords
    return df1_reshaped


def get_all_scale_data():
    infant = pd.read_csv('./data/infant.csv')
    adult = pd.read_csv('./data/300w.csv')
    mds_infant = pd.read_csv('./outcome/scale/mds_infant.csv')
    mds_adult = pd.read_csv('./outcome/scale/mds_adult.csv')
    norm_infant = pd.read_csv('./outcome/scale/normalized_infant.csv')
    norm_adult = pd.read_csv('./outcome/scale/normalized_adult.csv')
    std_infant = pd.read_csv('./outcome/scale/standard_infant.csv')
    std_adult = pd.read_csv('./outcome/scale/standard_adult.csv')
    return infant, adult, mds_infant, mds_adult, norm_infant, norm_adult, std_infant, std_adult
