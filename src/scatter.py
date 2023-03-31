import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据文件
df = pd.read_csv('outcome/prev/merged_landmarks.csv')

# 用循环计算以 "x" 和 "y" 开头的列的均值、中位数、标准差和范围
x_means = []
x_medians = []
x_stds = []
x_ranges = []
y_means = []
y_medians = []
y_stds = []
y_ranges = []

for i in range(68):
    x_col = 'x{}'.format(i)
    y_col = 'y{}'.format(i)
    x_data = df[x_col]
    y_data = df[y_col]
    x_mean = np.mean(x_data)
    x_median = np.median(x_data)
    x_std = np.std(x_data)
    x_range = np.max(x_data) - np.min(x_data)
    y_mean = np.mean(y_data)
    y_median = np.median(y_data)
    y_std = np.std(y_data)
    y_range = np.max(y_data) - np.min(y_data)
    x_means.append(x_mean)
    x_medians.append(x_median)
    x_stds.append(x_std)
    x_ranges.append(x_range)
    y_means.append(y_mean)
    y_medians.append(y_median)
    y_stds.append(y_std)
    y_ranges.append(y_range)


# 输出结果
for i in range(68):
    print('Column x{}: Mean={:.2f}, Median={:.2f}, Std={:.2f}, Range={:.2f}'.format(i, x_means[i], x_medians[i], x_stds[i], x_ranges[i]))
    print('Column y{}: Mean={:.2f}, Median={:.2f}, Std={:.2f}, Range={:.2f}'.format(i, y_means[i], y_medians[i], y_stds[i], y_ranges[i]))

'''
for i, (x, y) in enumerate(zip(x_mean, y_mean)):
    plt.scatter(x, y)
    plt.text(x + 0.02, y + 0.02, str(i), fontsize=10)
'''

plt.scatter(x_means, y_means)

# 标注每个点的序号
for i in range(len(x_means)):
    plt.annotate(str(i), (x_means[i], y_means[i]))

# 设置坐标轴标签和标题
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot of Landmarks')
# 显示图形
plt.savefig('outcome/outlier_selection/scatter.png')
plt.show()

# 提取需要绘制boxplot的列
columns1 = ['x{}'.format(i) for i in range(68)]

plt.xticks(fontproperties='Times New Roman', size=6)

plt.boxplot = df.boxplot(
    column=columns1)

plt.savefig('outcome/outlier_selection/boxplot_x.png')
plt.show()

# 提取需要绘制boxplot的列
columns1 = ['y{}'.format(i) for i in range(68)]

plt.xticks(fontproperties='Times New Roman', size=6)

plt.boxplot = df.boxplot(
    column=columns1)

plt.savefig('outcome/outlier_selection/boxplot_y.png')
plt.show()
'''
columns = ['x{}'.format(i) for i in range(68)]
data = df[columns]
# 绘制boxplot
fig, ax = plt.subplots(figsize=(12, 6))
ax.boxplot(data.values, labels=columns)
ax.set_title('Boxplot of Facial Landmarks')
ax.set_xlabel('Facial Landmark Index')
ax.set_ylabel('Coordinate Value')
plt.savefig('outcome/outlier_selection/boxplot.png')
plt.show()
'''








