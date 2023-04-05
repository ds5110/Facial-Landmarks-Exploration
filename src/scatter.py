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
    y_means = []

    for i in range(68):
        x_col = 'norm_cenrot-x{}'.format(i)
        y_col = 'norm_cenrot-y{}'.format(i)
        x_mean = np.mean(df[x_col])
        x_means.append(x_mean)
        x_median = np.median(df[x_col])
        x_std = np.std(df[x_col])
        x_range = np.max(df[x_col]) - np.min(df[x_col])
        y_mean = np.mean(df[y_col])
        y_means.append(y_mean)
        y_median = np.median(df[y_col])
        y_std = np.std(df[y_col])
        y_range = np.max(df[y_col]) - np.min(df[y_col])
        print('Column x{}: Mean={:.2f}, Median={:.2f}, Std={:.2f}, Range={:.2f}'.format(i, x_mean, x_median,
                                                                                        x_std, x_range))
        print('Column y{}: Mean={:.2f}, Median={:.2f}, Std={:.2f}, Range={:.2f}'.format(i, y_mean, y_median,
                                                                                        y_std, y_range))


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
