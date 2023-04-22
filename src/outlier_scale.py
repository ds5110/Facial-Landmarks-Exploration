import pandas as pd
from pandas.errors import PerformanceWarning

from outlier import make_noise
from outlier import ma
from outlier import isolation
import warnings

warnings.filterwarnings("ignore")

# Data was classified using three different scaling methods, and then further categorized into adult and infant
data = pd.read_csv('outcome/scale/rotated_scale.csv')

standard = data[data['scale_type'] == 'standard']
normalized = data[data['scale_type'] == 'normalized']
mds = data[data['scale_type'] == 'mds']

infant_standard = standard[standard['baby'] == 1]
adult_standard = standard[standard['baby'] == 0]

infant_normalized = normalized[normalized['baby'] == 1]
adult_normalized = normalized[normalized['baby'] == 0]

infant_mds = mds[mds['baby'] == 1]
adult_mds = mds[mds['baby'] == 0]


# get the x{} and y{} columns from the data and return the six formed data
def data(df_previous):
    df = pd.DataFrame()
    for i in range(68):
        x_col = 'x{}'.format(i)
        y_col = 'y{}'.format(i)
        df['x{}'.format(i)] = df_previous[x_col]
        df['y{}'.format(i)] = df_previous[y_col]
    df = pd.concat([df.filter(regex='^x'), df.filter(regex='^y')], axis=1)
    # df.to_csv("dd.csv", index=False)
    return df


# Evaluate efficiency of three scaling techniques by using two outlier detection model on datasets obtained from
# these methods.
def input_type(infant, adult):
    dfi = data(infant)
    dfa = data(adult)
    dfi_after, dfa_after = make_noise(dfi, dfa)

    print("Use isolation tree:")
    print("Test the method with noise:")
    print("infant_outlier:")
    isolation(dfi_after)
    print("adult_outlier:")
    isolation(dfa_after)

    print("------------------------------------------------------------")
    print("Use Mahalanobis:")
    print("Test the method with noise:")
    print("infant_outlier:")
    ma(dfi_after)
    print("adult_outlier:")
    ma(dfa_after)


if __name__ == '__main__':
    # Standard
    input_type(infant_standard, adult_standard)
    # Normalized
    input_type(infant_normalized, adult_normalized)
    # Mds
    input_type(infant_mds, adult_mds)
