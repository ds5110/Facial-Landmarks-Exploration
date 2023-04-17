import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from pandas.errors import PerformanceWarning
from sklearn.covariance import MinCovDet
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings('ignore', category=PerformanceWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# read the csv files
landmarks = pd.read_csv('outcome/prev/merged_landmarks.csv')
infant = landmarks[landmarks['baby'] == 1]
adult = landmarks[landmarks['baby'] == 0]


# get the norm_cenrot-x{} and norm_cenrot-y{} columns from the data and return the formed data
def data(df_previous):
    df = pd.DataFrame()
    # fix warning
    # another way to change the name of the columns
    """
    for i in range(68):
        x_col = 'norm_cenrot-x{}'.format(i)
        df['x{}'.format(i)] = df_previous[x_col]
    for i in range(68):
        y_col = 'norm_cenrot-y{}'.format(i)
        df['y{}'.format(i)] = df_previous[y_col]
        # df.to_csv("d.csv", index=False)
    """
    for i in range(68):
        x_col = 'norm_cenrot-x{}'.format(i)
        y_col = 'norm_cenrot-y{}'.format(i)
        df['x{}'.format(i)] = df_previous[x_col]
        df['y{}'.format(i)] = df_previous[y_col]
    df = pd.concat([df.filter(regex='^x'), df.filter(regex='^y')], axis=1)
    # df.to_csv("dd.csv", index=False)
    return df


# create some noise data and add to the end of the data
def make_noise(dfi, dfa):
    # df is the raw data
    print("Before:")
    print(dfi.shape)
    rows_i = math.floor(dfi.shape[0] * 0.05)
    print(dfa.shape)
    rows_a = math.floor(dfa.shape[0] * 0.05)

    # random data_ : the noise data
    # name the columns:very important
    col_names = ['x{}'.format(i) for i in range(68)] + ['y{}'.format(i) for i in range(68)]
    random_data_i = np.random.uniform(-1, 1, size=(rows_i, 136))
    random_data_a = np.random.uniform(-1, 1, size=(rows_a, 136))
    random_data_i = pd.DataFrame(random_data_i, columns=col_names)
    random_data_a = pd.DataFrame(random_data_a, columns=col_names)
    print(random_data_i.shape)
    print(random_data_a.shape)
    # print(random_data_i.iloc[18, 67])
    # data that added 5% random data at the end the file
    # the noise index is 410-429  689-722
    print("After:")
    dfi_after = pd.concat([dfi, random_data_i], axis=0)
    print(dfi_after.shape)
    dfi_after.to_csv("dfi_after.csv", index=False)
    dfa_after = pd.concat([dfa, random_data_a], axis=0)
    print(dfa_after.shape)
    dfa_after.to_csv("dfa_after.csv", index=False)
    return dfi_after, dfa_after


# use the Mahalanobis distance method to select the outlier
def ma(df):
    feature_cols = df.columns[:]
    # Calculate Mahalanobis distance
    mcd = MinCovDet().fit(df[feature_cols])
    mahal_dist = mcd.mahalanobis(df[feature_cols])
    # Determine the threshold for outlier detection
    threshold = np.quantile(mahal_dist, 41 / 43)
    outliers_index = np.where(np.array(mahal_dist) > threshold)[0]
    # Filter out outliers
    outliers = df[mahal_dist > threshold]
    print(outliers_index)


# use the isolation tree method to select the outlier
def isolation(df):
    clf = IsolationForest(random_state=0, contamination=2 / 43).fit(df)
    # clf = IsolationForest(n_estimators=100, contamination=0.05)

    y_pred = clf.predict(df)

    # outliers and filtered data
    outliers = df.reset_index().index[y_pred == -1]
    print("Outliers:", outliers)


# use the methods above to select the outlier from the raw data and the data which added noise
def main():
    dfi = data(infant)
    dfa = data(adult)
    dfi_after, dfa_after = make_noise(dfi, dfa)

    print("Use isolation tree:")
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

    print("------------------------------------------------------------")
    print("Use Mahalanobis:")
    print("Test the method with noise:")
    print("infant_outlier:")
    ma(dfi_after)
    print("adult_outlier:")
    ma(dfa_after)

    print("Data:")
    print("infant_outlier:")
    ma(dfi)
    print("adult_outlier:")
    ma(dfa)


if __name__ == '__main__':
    main()
