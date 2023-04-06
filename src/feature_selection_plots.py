import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("outcome/prev/merged_landmarks.csv")
x_cols = [col for col in df.columns if 'norm_cenrot-x' in col]
y_cols = [col for col in df.columns if 'norm_cenrot-y' in col]

x_mean = df[x_cols].mean(axis=0)
y_mean = df[y_cols].mean(axis=0)

fig, ax = plt.subplots()
x_abs_max = max(abs(x_mean))
y_abs_max = max(abs(y_mean))
ax.set_xlim([-x_abs_max, x_abs_max])
ax.set_ylim([-y_abs_max, y_abs_max])
ax.scatter(x_mean, y_mean, alpha=0.5)

ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)

selected_features = ['norm_cenrot-y6', 'norm_cenrot-y7', 'norm_cenrot-x8', 'norm_cenrot-y9', 'norm_cenrot-x21', 'norm_cenrot-x22', 'norm_cenrot-x23', 'norm_cenrot-x25', 'norm_cenrot-y28', 'norm_cenrot-x30', 'norm_cenrot-y30', 'norm_cenrot-x34', 'norm_cenrot-x38', 'norm_cenrot-y40', 'norm_cenrot-x42', 'norm_cenrot-x47', 'norm_cenrot-y48', 'norm_cenrot-y53', 'norm_cenrot-x55', 'norm_cenrot-y60']
for feature in selected_features:
    landmark_label = feature.split("-")[1]
    if feature in x_cols:
        landmark_x = x_mean[feature]
        landmark_y = y_mean[x_cols.index(feature)]
        ax.scatter(landmark_x, landmark_y, c="green")
        ax.annotate(landmark_label, (landmark_x, landmark_y), textcoords="offset points", xytext=(-5,-5))
        if landmark_x > 0:
            ax.axhline(y=landmark_y, xmin=0.5, xmax=0.5 + landmark_x / ax.get_xlim()[1] / 2, color='green', linewidth=0.5)
        if landmark_x < 0:
            ax.axhline(y=landmark_y, xmax=0.5, xmin=0.5 + landmark_x / ax.get_xlim()[1] / 2, color='green', linewidth=0.5)

    if feature in y_cols:
        landmark_x = x_mean[y_cols.index(feature)]
        landmark_y = y_mean[feature]
        ax.scatter(landmark_x, landmark_y, c="green")
        ax.annotate(landmark_label, (landmark_x, landmark_y), textcoords="offset points", xytext=(5,5))
        if landmark_y > 0:
            ax.axvline(x=landmark_x, ymin=0.5, ymax=(0.5 + landmark_y / ax.get_ylim()[1] / 2), color='green', linewidth=0.5)
        if landmark_y < 0:
            ax.axvline(x=landmark_x, ymax=0.5, ymin=(0.5 + landmark_y / ax.get_ylim()[1] / 2), color='green', linewidth=0.5)

plt.show()