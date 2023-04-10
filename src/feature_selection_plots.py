import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def variance_matrix():
    placeholder


def confusion_matrix():
    placeholder


def landmark_plots(df, x_cols, y_cols, feature_selection_result):
    x_mean = df[x_cols].mean(axis=0)
    y_mean = df[y_cols].mean(axis=0)
    x_abs_max = max(abs(x_mean))
    y_abs_max = max(abs(y_mean))
    
    methods = ["f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regulation", 
               "random_forest_classifier"]
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            ax.set_xlim([x_abs_max, -x_abs_max])
            ax.set_ylim([y_abs_max, -y_abs_max])
            ax.scatter(x_mean, y_mean, alpha=0.5)

            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            
            feature_names = method_df.columns[method_df.iloc[i, :] == True]
            for feature_name in feature_names:
                landmark_label = feature_name.split("-")[1]
                if feature_name in x_cols:
                    landmark_x = x_mean[feature_name]
                    landmark_y = y_mean[x_cols.index(feature_name)]
                    ax.scatter(landmark_x, landmark_y, c="green")
                    ax.annotate(landmark_label, (landmark_x, landmark_y), textcoords="offset points", xytext=(-20, -10))
                    if landmark_x > 0:
                        ax.axhline(y=landmark_y, xmin=0.5, xmax=0.5 + landmark_x / ax.get_xlim()[1] / 2, color="green", linewidth=0.5)
                    else:
                        ax.axhline(y=landmark_y, xmax=0.5, xmin=0.5 + landmark_x / ax.get_xlim()[1] / 2, color="green", linewidth=0.5)

                if feature_name in y_cols:
                    landmark_x = x_mean[y_cols.index(feature_name)]
                    landmark_y = y_mean[feature_name]
                    ax.scatter(landmark_x, landmark_y, c="green")
                    ax.annotate(landmark_label, (landmark_x, landmark_y), textcoords="offset points", xytext=(5, 5))
                    if landmark_y > 0:
                        ax.axvline(x=landmark_x, ymin=0.5, ymax=(0.5 + landmark_y / ax.get_ylim()[1] / 2), color="green", linewidth=0.5)
                    else:
                        ax.axvline(x=landmark_x, ymax=0.5, ymin=(0.5 + landmark_y / ax.get_ylim()[1] / 2), color="green", linewidth=0.5)
            ax.set_title("{}\n CV Test Score = {:.3f} +/- {:.3f}".format(method_df.iloc[i, 0], method_df.iloc[i, 3], method_df.iloc[i, 4]), pad=20)
        fig.subplots_adjust(hspace=0.4)
        fig.savefig("outcome/feature_selection/features_{}.png".format(method), dpi=300)


def main():
    feature_selection_result = pd.read_csv("outcome/feature_selection/feature_selection.csv")
    df = pd.read_csv("outcome/prev/merged_landmarks.csv")
    
    feature_cols = [col for col in df.columns if 'norm_cenrot-' in col]
    x_cols = [col for col in df.columns if 'norm_cenrot-x' in col]
    y_cols = [col for col in df.columns if 'norm_cenrot-y' in col]

    landmark_plots(df, x_cols, y_cols, feature_selection_result)


if __name__ == "__main__":
    main()