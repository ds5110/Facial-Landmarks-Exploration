import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read the csv files
landmarks = pd.read_csv('outcome/prev/merged_landmarks.csv')
infant = landmarks[landmarks['baby'] == 1]
adult = landmarks[landmarks['baby'] == 0]


def scatter(df, category):
    # calculate the means, medians,stds,range of x,y
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

    # output the outcome
    for i in range(68):
        print('Column x{}: Mean={:.2f}, Median={:.2f}, Std={:.2f}, Range={:.2f}'.format(i, x_means[i], x_medians[i],
                                                                                        x_stds[i], x_ranges[i]))
        print('Column y{}: Mean={:.2f}, Median={:.2f}, Std={:.2f}, Range={:.2f}'.format(i, y_means[i], y_medians[i],
                                                                                        y_stds[i], y_ranges[i]))

    '''
    for i, (x, y) in enumerate(zip(x_mean, y_mean)):
        plt.scatter(x, y)
        plt.text(x + 0.02, y + 0.02, str(i), fontsize=10)
    '''

    plt.scatter(x_means, y_means)

    # mark the order of the dot
    for i in range(len(x_means)):
        plt.annotate(str(i), (x_means[i], y_means[i]))

    # set the label and title
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Landmarks of ' + category)
    # show the fig
    plt.savefig('outcome/outlier_selection/scatter.png')
    plt.show()

    # choose the columns we need
    columns1 = ['norm_cenrot-x{}'.format(i) for i in range(68)]

    plt.boxplot = df.boxplot(
        column=columns1)

    # change the name of the columns
    x = [None] * 68
    for i in range(68):
        x[i] = columns1[i].split('-')[1]

    plt.gca().set_xticklabels(x)

    plt.xticks(fontproperties='Times New Roman', size=6)

    plt.savefig('outcome/outlier_selection/boxplot_x.png')
    plt.show()

    # choose the columns we need
    columns1 = ['norm_cenrot-y{}'.format(i) for i in range(68)]

    plt.boxplot = df.boxplot(
        column=columns1)

    # change the name of xticks
    y = [None] * 68
    for i in range(68):
        y[i] = columns1[i].split('-')[1]

    plt.gca().set_xticklabels(y)

    plt.xticks(fontproperties='Times New Roman', size=6)

    plt.savefig('outcome/outlier_selection/boxplot_y.png')
    plt.show()


scatter(infant, "infant")

scatter(adult, "adult")


