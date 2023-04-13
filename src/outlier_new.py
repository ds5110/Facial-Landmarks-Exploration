import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from sklearn.covariance import MinCovDet
from sklearn.ensemble import IsolationForest

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


# df is the raw data
print("Before:")
dfi = data(infant)
print(dfi.shape)
rows_i = math.floor(dfi.shape[0] * 0.05)
dfa = data(adult)
print(dfa.shape)
rows_a = math.floor(dfa.shape[0] * 0.05)

col_names_i = [f'x{i}' for i in range(68)]
col_names_a = [f'x{i}' for i in range(68)]

# random data_ : the noise data
random_data_i = np.random.uniform(-1, 1, size=(rows_i, 68))
random_data_a = np.random.uniform(-1, 1, size=(rows_a, 68))
random_data_i = pd.DataFrame(random_data_i, columns=col_names_i)
random_data_a = pd.DataFrame(random_data_a, columns=col_names_a)
# print(random_data_i.shape)
# print(random_data_i.iloc[18, 67])
# data that added 5% random data at the end the file
# the noise index is 411-430  690-723

print("After:")
dfi_after = pd.concat([dfi, random_data_i], axis=0)
print(dfi_after.shape)
dfi_after.to_csv("dfi_after.csv", index=False)
dfa_after = pd.concat([dfa, random_data_a], axis=0)
print(dfa_after.shape)
dfa_after.to_csv("dfa_after.csv", index=False)


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


def isolation(df):

    clf = IsolationForest(random_state=0, contamination=0.05).fit(df)
    #clf = IsolationForest(n_estimators=100, contamination=0.05)

    y_pred = clf.predict(df)

    # outliers and filtered data
    outliers = df.reset_index().index[y_pred == -1]
    print("Outliers:", outliers)

'''
print("Test the method with noise:")
print("infant_outlier:")
outlier_selection(dfi_after)
print("adult_outlier:")
outlier_selection(dfa_after)


print("Data:")
print("infant_outlier:")
outlier_selection(dfi)
print("adult_outlier:")
outlier_selection(dfa)
'''

print("Test the method with noise:")
print("infant_outlier:")
isolation(dfi_after)
print("adult_outlier:")
isolation(dfa_after)


print("Data:")
print("infant_outlier:")
isolation(dfi)
print("adult_outlier:")
isolation(dfa)

