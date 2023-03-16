import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.covariance import MinCovDet

# Read data from CSV file
df1 = pd.read_csv('outcome/outlier_selection/euclidean_part_adult.csv')
df2 = pd.read_csv('outcome/outlier_selection/euclidean_part_adult.csv')


def outliers(df):
    # Select feature columns
    feature_cols = df.columns[1:]  # Ignore the first column since it's an index column

    # Calculate Mahalanobis distance
    mcd = MinCovDet().fit(df[feature_cols])
    mahal_dist = mcd.mahalanobis(df[feature_cols])

    # Determine the threshold for outlier detection
    threshold = np.quantile(mahal_dist, 0.95)

    # Filter out outliers
    outliers = df[mahal_dist > threshold]

    # the data after filtering
    filtered_df = df[mahal_dist <= threshold]

    pca = PCA(n_components=2)
    pca.fit(df[feature_cols])
    projected = pca.transform(df[feature_cols])
    outliers_projected = pca.transform(outliers[feature_cols])

    '''
    For data with 2278 columns, we cannot directly plot a scatter plot of all features 
    to visualize the data and outliers. One possible approach is to use principal component
    analysis (PCA) to project the data into a lower dimensional space and visualize 
    the data points in this space.'''
    plt.scatter(projected[:, 0], projected[:, 1], color='b', alpha=0.5)
    plt.scatter(outliers_projected[:, 0], outliers_projected[:, 1], color='r')
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Scatter Plot with Outliers (PCA)')
    plt.show()
    return outliers, filtered_df


outliers_infant,filtered_df_infant= outliers(df1)
outliers_infant.to_csv('outcome/outlier_selection/outliers_infant.csv', index=False)
filtered_df_infant.to_csv('outcome/outlier_selection/filtered_infant.csv', index=False)


outliers_adult,filtered_df_adult= outliers(df2)
outliers_adult.to_csv('outcome/outlier_selection/outliers_adult.csv', index=False)
filtered_df_adult.to_csv('outcome/outlier_selection/filtered_adult.csv', index=False)


