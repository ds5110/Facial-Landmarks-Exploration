import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.covariance import MinCovDet

# Read data from CSV file
df = pd.read_csv('outcome/outlier_selection/euclidean_part_infant.csv')

# Select feature columns
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

# output outliers
#outliers.to_csv('outcome/outlier_selection/outliers_infant_ma.csv', index=False)

# filter out outliers
filtered_df = df[mahal_dist <= threshold]

# save the data after filtering
filtered_df.to_csv('outcome/outlier_selection/filtered_infant_ma.csv', index=False)
'''
For data with 2278 columns, we cannot directly plot a scatter plot of all features 
to visualize the data and outliers. One possible approach is to use principal component
analysis (PCA) to project the data into a lower dimensional space and visualize 
the data points in this space.

pca = PCA(n_components=2)
pca.fit(df[feature_cols])
projected = pca.transform(df[feature_cols])
outliers_projected = pca.transform(outliers[feature_cols])

plt.scatter(outliers_projected[:, 0], outliers_projected[:, 1], color='r')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Scatter Plot with Outliers (PCA)')
plt.show()
plt.savefig('outcome/outlier_selection/filtered_infant.png', dpi=300)
'''

# 使用PCA将数据投影到三维空间中
pca = PCA(n_components=3)
pca.fit(df[feature_cols])
projected = pca.transform(df[feature_cols])
outliers_projected = pca.transform(outliers[feature_cols])

# 绘制三维散点图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(projected[:, 0], projected[:, 1], projected[:, 2], color='b', alpha=0.5)
ax.scatter(outliers_projected[:, 0], outliers_projected[:, 1], outliers_projected[:, 2], color='r')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.set_title('Scatter Plot with Outliers (PCA)')

plt.savefig('outcome/outlier_selection/ma_infant.png')
# 显示图形
plt.show()
