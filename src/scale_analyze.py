from sklearn.metrics import mean_squared_error
from scipy.spatial import procrustes
import pandas as pd
import numpy as np
import utils

infant = pd.read_csv('./data/infant.csv')
adult = pd.read_csv('./data/300w.csv')
mds_infant = pd.read_csv('./outcome/scale/mds_infant.csv')
mds_adult = pd.read_csv('./outcome/scale/mds_adult.csv')
norm_infant = pd.read_csv('./outcome/scale/normalized_infant.csv')
norm_adult = pd.read_csv('./outcome/scale/normalized_adult.csv')
std_infant = pd.read_csv('./outcome/scale/standard_infant.csv')
std_adult = pd.read_csv('./outcome/scale/standard_adult.csv')

columns = ['Infant', 'Adult']
rows = ['MDS', 'Standard', 'NormalizedByFaceBoundingBox']
infant_cols, infant_x_cols, infant_y_cols = utils.get_infant_cols(infant)
adult_cols, adult_x_cols, adult_y_cols = utils.get_adult_cols(adult)

mse_table = pd.DataFrame(columns=columns, index=rows)
mse_table.loc['MDS', 'Infant'] = mean_squared_error(infant[infant_cols].values, mds_infant[infant_cols].values)
mse_table.loc['MDS', 'Adult'] = mean_squared_error(adult[adult_cols].values, mds_adult[adult_cols].values)
mse_table.loc['Standard', 'Infant'] = mean_squared_error(infant[infant_cols].values, std_infant[infant_cols].values)
mse_table.loc['Standard', 'Adult'] = mean_squared_error(adult[adult_cols].values, std_adult[adult_cols].values)
mse_table.loc['NormalizedByFaceBoundingBox', 'Infant'] = mean_squared_error(infant[infant_cols].values,
                                                                            norm_infant[infant_cols].values)
mse_table.loc['NormalizedByFaceBoundingBox', 'Adult'] = mean_squared_error(adult[adult_cols].values,
                                                                           norm_adult[adult_cols].values)
print("MSE TABLE", mse_table)


def calculate_infant_procrustes(df1, df2):
    return calculate_procrustes(df1, df2, infant_x_cols, infant_y_cols)


def calculate_procrustes(df1, df2, x_cols, y_cols):
    df1_reshaped = utils.reshape_to_2d(df1, x_cols, y_cols)
    df2_reshaped = utils.reshape_to_2d(df2, x_cols, y_cols)
    disparities = []
    for i in range(df1_reshaped.shape[0]):
        mtx1, mtx2, disparity = procrustes(df1_reshaped[i], df2_reshaped[i])
        disparities.append(disparity)
    mean_disparity = np.mean(disparities)
    return mean_disparity


def calculate_adult_procrustes(df1, df2):
    return calculate_procrustes(df1, df2, adult_x_cols, adult_y_cols)


proc_table = pd.DataFrame(columns=columns, index=rows)
proc_table.loc['MDS', 'Infant'] = calculate_infant_procrustes(infant, mds_infant)
proc_table.loc['MDS', 'Adult'] = calculate_adult_procrustes(adult, mds_adult)
proc_table.loc['Standard', 'Infant'] = calculate_infant_procrustes(infant, std_infant)
proc_table.loc['Standard', 'Adult'] = calculate_adult_procrustes(adult, std_adult)
proc_table.loc['NormalizedByFaceBoundingBox', 'Infant'] = calculate_infant_procrustes(infant, norm_infant)
proc_table.loc['NormalizedByFaceBoundingBox', 'Adult'] = calculate_adult_procrustes(adult, norm_adult)
print("Procrustes Distance", proc_table)
