from sklearn.ensemble import IsolationForest
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


df = pd.read_csv('outcome/outlier_selection/euclidean_part_infant.csv')
feature_cols = df.columns[:]

# define model
clf = IsolationForest(n_estimators=100, contamination=0.05)

# fit model
clf.fit(df[feature_cols])
y_pred = clf.predict(df[feature_cols])

# outliers and filtered data
outliers = df[y_pred == -1]
print("Outliers:", outliers)

filtered_df = df[y_pred != -1]
filtered_df.to_csv('outcome/outlier_selection/filtered_infant_if.csv', index=False)

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

plt.savefig('outcome/outlier_selection/isolation_forest_infant.png')
# 显示图形
plt.show()

