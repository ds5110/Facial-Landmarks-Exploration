import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from utils import get_data, get_data_scale, get_cols, get_cols_scale


def variance_dotplot(df, address, title):
    fig = plt.figure(figsize=(5, 3))
    var = df.var()
    ax = sns.stripplot(data=var, orient="h", size=3)
    ax.set(xlabel="Variances", ylabel="Features", title=title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close()


def correlation_matrix(df, address, title):
    fig = plt.figure(figsize=(5, 5))
    cor = df.corr(numeric_only=True).abs()
    ax = sns.heatmap(cor, cmap="flare")
    ax.set(xlabel="", ylabel="", title=title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close()


def get_mean_landmark(df, x_cols, y_cols):
    x_mean = df[x_cols].mean(axis=0)
    y_mean = df[y_cols].mean(axis=0)
    x_abs_max = max(abs(x_mean))
    y_abs_max = max(abs(y_mean))
    return x_mean, y_mean, x_abs_max, y_abs_max


def mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max):
    ax.set(xlim=[x_abs_max, -x_abs_max], ylim=[y_abs_max, -y_abs_max])
    ax.scatter(x_mean, y_mean, alpha=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)


def landmark_plots(df, x_cols, y_cols, feature_selection_result, methods, address):
    x_mean, y_mean, x_abs_max, y_abs_max = get_mean_landmark(df, x_cols, y_cols)
    
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max)
            
            feature_names = method_df.columns[method_df.iloc[i, :] == True]
            for feature_name in feature_names:
                landmark_label = feature_name.split("-")[-1]
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
        fig.savefig("{}/landmarks_{}.png".format(address, method), dpi=300)

        print("Saved: {}/landmarks_{}.png".format(address, method))
        plt.close()


def euclidean_plots(df, feature_cols, x_cols, y_cols, feature_selection_result, methods, address):
    x_mean, y_mean, x_abs_max, y_abs_max = get_mean_landmark(df, x_cols, y_cols)
    
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max)
            
            feature_names = method_df.columns[method_df.iloc[i, :] == True]
            for feature_name in feature_names:
                landmark_label_1 = feature_name.split("_")[1]
                landmark_label_2 = feature_name.split("_")[2]
                landmark_1_x = x_mean[int(landmark_label_1)]
                landmark_1_y = y_mean[int(landmark_label_1)]
                landmark_2_x = x_mean[int(landmark_label_2)]
                landmark_2_y = y_mean[int(landmark_label_2)]

                ax.scatter(landmark_1_x, landmark_1_y, c="green")
                ax.scatter(landmark_2_x, landmark_2_y, c="green")
                ax.annotate(landmark_label_1, (landmark_1_x, landmark_1_y), textcoords="offset points", xytext=(5, 5))
                ax.annotate(landmark_label_2, (landmark_2_x, landmark_2_y), textcoords="offset points", xytext=(5, 5))
                ax.plot([landmark_1_x, landmark_2_x], [landmark_1_y, landmark_2_y], c="green")
            ax.set_title("{}\n CV Test Score = {:.3f} +/- {:.3f}".format(method_df.iloc[i, 0], method_df.iloc[i, 3], method_df.iloc[i, 4]), pad=20)
        fig.subplots_adjust(hspace=0.4)
        fig.savefig("{}/euclidean_{}.png".format(address, method), dpi=300)

        print("Saved: {}/euclidean_{}.png".format(address, method))
        plt.close()


def confusion_matrix(feature_selection_result, methods, euclidean, address):
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            cm = pd.DataFrame(data=method_df.iloc[i, 5:9].values.reshape(2, 2), index=["adult", "infant"], columns=["adult", "infant"])
            cm = cm.apply(pd.to_numeric)
            sns.heatmap(cm, cmap="flare", annot=True, cbar=False, fmt="d", ax=ax)
            ax.set(xlabel="Predicted Target", ylabel="True Target")
            ax.set_title("{}\n CV Test Score = {:.3f} +/- {:.3f}".format(method_df.iloc[i, 0], method_df.iloc[i, 3], method_df.iloc[i, 4]))
        fig.subplots_adjust(hspace=0.4)
        fig.savefig("{}/confusion_matrix_{}_{}.png".format(address, "landmarks" if euclidean==True else "euclidean", method), dpi=300)

        print("Saved: {}/confusion_matrix_{}_{}.png".format(address, "landmarks" if euclidean==True else "euclidean", method))
        plt.close()


def method_score_plot(feature_selection_result, methods, n_features, address, title):
    fig= plt.figure(figsize=(10, 5))
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        ax1.plot(n_features, method_df["CV_train_score_mean"], label="{} Train Score".format(method))
        ax2.plot(n_features, method_df["CV_test_score_mean"], label="{} Test Score".format(method))
    ax1.axhline(y=0.9, linestyle="dashed")
    ax2.axhline(y=0.9, linestyle="dashed")
    ax1.legend()
    ax2.legend()
    fig.suptitle(title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close()


def main():
    methods = ["f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regulation", 
               "random_forest_classifier"]
    n_features = [2, 3, 5, 10, 15, 20, 30, 50]

    # Landmark plots
    print("========Landmark Feature Plots========")

    feature_selection_result = pd.read_csv("outcome/feature_selection/feature_selection_landmarks.csv")
    df = get_data("outcome/prev/merged_landmarks.csv")
    x_cols, y_cols = get_cols(df)
    feature_cols = [col for col in df.columns if 'norm_cenrot-' in col]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection/variance_dotplot_landmarks.png", "Variance Dotplot of All Landmark Features")
    correlation_matrix(df_X, "outcome/feature_selection/correlation_matrix_landmarks.png", "Correlation Matrix of All Landmark Features")
    landmark_plots(df, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection/method_scores_landmarks.png", "CV Scores of All Landmark Selection Methods")
    confusion_matrix(feature_selection_result, methods, False, "outcome/feature_selection")

    # Euclidean distance plots
    print("========Euclidean Feature Plots========")

    feature_selection_result = pd.read_csv("outcome/feature_selection/feature_selection_euclidean.csv")
    df = get_data("outcome/euclidean/euclidean_merged.csv")
    x_cols, y_cols = get_cols(df)
    feature_cols = [col for col in df.columns if 'dist_' in col]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection/variance_dotplot_euclidean.png", "Variance Dotplot of All Euclidean Distance Features")
    correlation_matrix(df_X, "outcome/feature_selection/correlation_matrix_euclidean.png", "Correlation Matrix of All Euclidean Distance Features")
    euclidean_plots(df, feature_cols, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection/method_scores_euclidean.png", "CV Scores of All Euclidean Distance Selection Methods")
    confusion_matrix(feature_selection_result, methods, True, "outcome/feature_selection")


def main_scale():
    methods = ["f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regulation", 
               "random_forest_classifier"]
    n_features = [2, 3, 5, 10, 15, 20, 30, 50]

    # Landmark plots
    print("========Landmark Feature Plots (Scale Method)========")

    feature_selection_result = pd.read_csv("outcome/feature_selection_scale/feature_selection_landmarks.csv")
    df = get_data_scale("outcome/scale/rotated_scale.csv")
    x_cols, y_cols = get_cols_scale(df)
    feature_cols = [col for col in df.columns if col.startswith("x") or col.startswith("y")]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection_scale/variance_dotplot_landmarks.png", "Variance Dotplot of All Landmark Features Using Scale Method")
    correlation_matrix(df_X, "outcome/feature_selection_scale/correlation_matrix_landmarks.png", "Correlation Matrix of All Landmark Features Using Scale Method")
    landmark_plots(df, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection_scale")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection_scale/method_scores_landmarks.png", "CV Scores of All Landmark Selection Methods Using Scale Method")
    confusion_matrix(feature_selection_result, methods, False, "outcome/feature_selection_scale")

    # Euclidean distance plots
    print("========Euclidean Feature Plots (Scale Method)========")

    feature_selection_result = pd.read_csv("outcome/feature_selection_scale/feature_selection_euclidean.csv")
    df = get_data_scale("outcome/euclidean/euclidean_merged_scale.csv")
    x_cols, y_cols = get_cols_scale(df)
    feature_cols = [col for col in df.columns if 'dist_' in col]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection_scale/variance_dotplot_euclidean.png", "Variance Dotplot of All Euclidean Distance Features Using Scale Method")
    correlation_matrix(df_X, "outcome/feature_selection_scale/correlation_matrix_euclidean.png", "Correlation Matrix of All Euclidean Distance Features Using Scale Method")
    euclidean_plots(df, feature_cols, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection_scale")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection_scale/method_scores_euclidean.png", "CV Scores of All Euclidean Distance Selection Methods Using Scale Method")
    confusion_matrix(feature_selection_result, methods, True, "outcome/feature_selection_scale")


if __name__ == "__main__":
    main()
    # main_scale()