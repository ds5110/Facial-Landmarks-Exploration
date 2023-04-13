import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.covariance import MinCovDet

# read the csv files
landmarks = pd.read_csv('outcome/prev/merged_landmarks.csv')
infant = landmarks[landmarks['baby'] == 1]
adult = landmarks[landmarks['baby'] == 0]


def data(df_previous):
    df = pd.DataFrame()
    for i in range(68):
        x_col = 'norm_cenrot-x{}'.format(i)
        y_col = 'norm_cenrot-y{}'.format(i)
        df['x{}'.format(i)] = df_previous[x_col]
    return df


print("Before:")
dfi = data(infant)
print(dfi.shape)
rows_i = math.floor(dfi.shape[0] * 0.05)
dfa = data(adult)
print(dfa.shape)
rows_a = math.floor(dfa.shape[0] * 0.05)

col_names_i = [f'x{i}' for i in range(68)]
col_names_a = [f'x{i}' for i in range(68)]
random_data_i = np.random.uniform(-1, 1, size=(rows_i, 68))
random_data_a = np.random.uniform(-1, 1, size=(rows_a, 68))
random_data_i = pd.DataFrame(random_data_i, columns=col_names_i)
random_data_a = pd.DataFrame(random_data_a, columns=col_names_a)
# print(random_data_i.shape)
# print(random_data_i.iloc[18, 67])
# data that added 5% random data at the end the file
# the noise index is 411-430  690-723

print("After:")
dfi = pd.concat([dfi, random_data_i], axis=0)
print(dfi.shape)
dfi.to_csv("dfi_after.csv", index=False)
dfa = pd.concat([dfa, random_data_a], axis=0)
print(dfa.shape)
dfa.to_csv("dfa_after.csv", index=False)
print(dfi.iloc[420, 67])


def outlier_selection(df):
    feature_cols = df.columns[:]
    # Calculate Mahalanobis distance
    mcd = MinCovDet().fit(df[feature_cols])
    mahal_dist = mcd.mahalanobis(df[feature_cols])
    # Determine the threshold for outlier detection
    threshold = np.quantile(mahal_dist, 0.95)
    outliers_index = np.where(np.array(mahal_dist) > threshold)[0]
    # Filter out outliers
    outliers = df[mahal_dist > threshold]
    print(outliers_index)


print("infant:")
outlier_selection(dfi)
print("adult:")
outlier_selection(dfa)
