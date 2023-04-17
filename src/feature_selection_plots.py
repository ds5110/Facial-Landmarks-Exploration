import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
from utils import get_data, get_data_scale, get_cols, get_cols_scale


# Generate dot plots to show variance distribution of features
def variance_dotplot(df, address, title):
    fig = plt.figure(figsize=(15, 4))
    var = df.var()
    ax = sns.stripplot(data=var, orient="h", size=3)
    ax.set(xlabel="Variances", ylabel="Features", title=title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close(fig)


# Generate heatmaps to show the correlation between features
def correlation_matrix(df, address, title):
    fig = plt.figure(figsize=(15, 8))
    cor = df.corr(numeric_only=True).abs()
    ax = sns.heatmap(cor, cmap="flare")
    ax.set(xlabel="", ylabel="", title=title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close(fig)


# Calculate the mean x and y coordinates of landmarks and their value range
def get_mean_landmark(df, x_cols, y_cols):
    x_mean = df[x_cols].mean(axis=0)
    y_mean = df[y_cols].mean(axis=0)
    x_abs_max = max(abs(x_mean))
    y_abs_max = max(abs(y_mean))
    return x_mean, y_mean, x_abs_max, y_abs_max


# Generate scatter plots to show all landmarks with mean coordinates
def mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max):
    ax.set(xlim=[x_abs_max, -x_abs_max], ylim=[y_abs_max, -y_abs_max])
    ax.scatter(x_mean, y_mean, alpha=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)


# Generate scatter plots to show landmarks selected as features
# Generate lines to show x and y coordinates directions
def landmark_feature_plot(i, ax, x_cols, y_cols, method_df, x_mean, y_mean):
    feature_names = method_df.columns[method_df.iloc[i, :] == True]
    for feature_name in feature_names:
        landmark_label = feature_name.split("-")[-1]

        # x-coordinates as features
        if feature_name in x_cols:
            landmark_x = x_mean[feature_name]
            landmark_y = y_mean[x_cols.index(feature_name)]
            ax.scatter(landmark_x, landmark_y, c="green")
            ax.annotate(landmark_label, (landmark_x, landmark_y), textcoords="offset points", xytext=(-20, -10))
            
            # Lines to show coordinate directions
            if landmark_x > 0:
                ax.axhline(y=landmark_y, xmin=0.5, xmax=0.5 + landmark_x / ax.get_xlim()[1] / 2, color="green", linewidth=0.5)
            else:
                ax.axhline(y=landmark_y, xmax=0.5, xmin=0.5 + landmark_x / ax.get_xlim()[1] / 2, color="green", linewidth=0.5)
        
        # y-coordinates as features
        if feature_name in y_cols:
            landmark_x = x_mean[y_cols.index(feature_name)]
            landmark_y = y_mean[feature_name]
            ax.scatter(landmark_x, landmark_y, c="green")
            ax.annotate(landmark_label, (landmark_x, landmark_y), textcoords="offset points", xytext=(5, 5))
            
            # Lines to show coordinate directions
            if landmark_y > 0:
                ax.axvline(x=landmark_x, ymin=0.5, ymax=(0.5 + landmark_y / ax.get_ylim()[1] / 2), color="green", linewidth=0.5)
            else:
                ax.axvline(x=landmark_x, ymax=0.5, ymin=(0.5 + landmark_y / ax.get_ylim()[1] / 2), color="green", linewidth=0.5)
    
    # Show selector name and test scores in subtitles
    ax.set_title("{}\n CV Test Score = {:.3f} +/- {:.3f}".format(method_df.iloc[i, 0], method_df.iloc[i, 5], method_df.iloc[i, 6]), pad=20)


# Call `mean_landmark_plot` and `landmark_feature_plot` to generate plots for each feature selection method
# Each method plot would contain 8 subplots, with each representing one selector
def landmark_plots(df, x_cols, y_cols, feature_selection_result, methods, address):
    x_mean, y_mean, x_abs_max, y_abs_max = get_mean_landmark(df, x_cols, y_cols)
    
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max)
            landmark_feature_plot(i, ax, x_cols, y_cols, method_df, x_mean, y_mean)  
        
        fig.subplots_adjust(hspace=0.4)
        fig.savefig("{}/landmarks_{}.png".format(address, method), dpi=300)

        print("Saved: {}/landmarks_{}.png".format(address, method))
        plt.close(fig)


# Set a criterion to select "good" selection results
def get_best_selectors(feature_selection_result):
    best_selector_names = []
    method_names = []
    for i in range(1, feature_selection_result.shape[0]):
        selector_name = feature_selection_result.iloc[i, 0]
        method_name = feature_selection_result.iloc[i, 1]
        test_score = feature_selection_result.iloc[i, 5]
        if test_score > 0.88 and method_name not in method_names:
            best_selector_names.append(selector_name)
            method_names.append(method_name)
            
    return best_selector_names


# Call `get_best_selectors` to get "good" selection results of landmarks
# Call `mean_landmark_plot` and `landmark_feature_plot` to generate plots for them
def best_landmark_plots(df, x_cols, y_cols, feature_selection_result, address):
    x_mean, y_mean, x_abs_max, y_abs_max = get_mean_landmark(df, x_cols, y_cols)
    best_selector_names = get_best_selectors(feature_selection_result)
    selector_df = feature_selection_result.loc[feature_selection_result["selector_name"].isin(best_selector_names)]
    
    figrows = len(best_selector_names) // 4 + (len(best_selector_names) % 4 > 0)
    fig, axs = plt.subplots(figrows, 4, figsize=(20, figrows * 5))
    for i in range(len(best_selector_names)):
        ax = axs.flat[i]
        mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max)
        landmark_feature_plot(i, ax, x_cols, y_cols, selector_df, x_mean, y_mean)
    
    fig.subplots_adjust(hspace=0.4)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close(fig)


# Generate scatter plots to show landmarks that were selected to make up distance features
# Generate lines to show distances between pairs of landmarks
def euclidean_feature_plot(i, ax, method_df, x_mean, y_mean):
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
    
    # Show selector name and test scores in subtitles
    ax.set_title("{}\n CV Test Score = {:.3f} +/- {:.3f}".format(method_df.iloc[i, 0], method_df.iloc[i, 5], method_df.iloc[i, 6]), pad=20)


# Call `mean_landmark_plot` and `euclidean_feature_plot` to generate plots for each feature selection method
# Each method plot would contain 8 subplots, with each representing one selector
def euclidean_plots(df, feature_cols, x_cols, y_cols, feature_selection_result, methods, address):
    x_mean, y_mean, x_abs_max, y_abs_max = get_mean_landmark(df, x_cols, y_cols)
    
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max)
            euclidean_feature_plot(i, ax, method_df, x_mean, y_mean)
            
        fig.subplots_adjust(hspace=0.4)
        fig.savefig("{}/euclidean_{}.png".format(address, method), dpi=300)

        print("Saved: {}/euclidean_{}.png".format(address, method))
        plt.close(fig)



# Call `get_best_selectors` to get "good" selection results of Euclidean Distances
# Call `mean_landmark_plot` and `euclidean_feature_plot` to generate plots for them
def best_euclidean_plots(df, x_cols, y_cols, feature_selection_result, address):
    x_mean, y_mean, x_abs_max, y_abs_max = get_mean_landmark(df, x_cols, y_cols)
    best_selector_names = get_best_selectors(feature_selection_result)
    selector_df = feature_selection_result.loc[feature_selection_result["selector_name"].isin(best_selector_names)]
    
    figrows = len(best_selector_names) // 4 + (len(best_selector_names) % 4 > 0)
    fig, axs = plt.subplots(figrows, 4, figsize=(20, figrows * 5))
    for i in range(len(best_selector_names)):
        ax = axs.flat[i]
        mean_landmark_plot(ax, x_mean, y_mean, x_abs_max, y_abs_max)
        euclidean_feature_plot(i, ax, selector_df, x_mean, y_mean)
    
    fig.subplots_adjust(hspace=0.4)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close(fig)
    

# Generate heatmaps to show confusion matrices of feature selection results
# Can be used for both landmark and Euclidean Distance results, determined by the boolean parameter
def confusion_matrix(feature_selection_result, methods, euclidean, address):
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        fig, axs = plt.subplots(2, 4, figsize=(20, 10))
        for i, ax in enumerate(axs.flat):
            cm = pd.DataFrame(data=method_df.iloc[i, 7:11].values.reshape(2, 2), index=["adult", "infant"], columns=["adult", "infant"])
            cm = cm.apply(pd.to_numeric)
            ax = sns.heatmap(cm, cmap="flare", annot=True, cbar=False, fmt="d", ax=ax)
            ax.set(xlabel="Predicted Target", ylabel="True Target")
            # Show selector name and test scores in subtitles
            ax.set_title("{}\n CV Test Score = {:.3f} +/- {:.3f}".format(method_df.iloc[i, 0], method_df.iloc[i, 5], method_df.iloc[i, 6]))
        fig.subplots_adjust(hspace=0.4)
        fig.savefig("{}/confusion_matrix_{}_{}.png".format(address, "landmarks" if euclidean==False else "euclidean", method), dpi=300)

        print("Saved: {}/confusion_matrix_{}_{}.png".format(address, "landmarks" if euclidean==False else "euclidean", method))
        plt.close(fig)


# Generate line plots to show all cross-validation train and test scores
# for all feature selection results
def method_score_plot(feature_selection_result, methods, n_features, address, title):
    fig= plt.figure(figsize=(10, 5))
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)
    for method in methods:
        method_df = feature_selection_result.loc[feature_selection_result["selector_name"].str.contains(method)]
        ax1.plot(n_features, method_df["CV_train_score_mean"], label="{} Train Score".format(method))
        ax2.plot(n_features, method_df["CV_test_score_mean"], label="{} Test Score".format(method))
    
    all_feature_train_score = feature_selection_result.loc[feature_selection_result["method_name"]=="all_features", ["CV_train_score_mean"]].values[0]
    all_feature_test_score = feature_selection_result.loc[feature_selection_result["method_name"]=="all_features", ["CV_test_score_mean"]].values[0]
    ax1.axhline(y=all_feature_train_score, linestyle="dashed")
    ax2.axhline(y=all_feature_test_score, linestyle="dashed")

    ax1.axhline(y=0.9, linestyle="dashed")
    ax2.axhline(y=0.9, linestyle="dashed")
    ax1.legend()
    ax2.legend()
    fig.suptitle(title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close(fig)


# Generate heatmaps to show the running time for each feature selection selector
def selection_time_plot(feature_selection_result, address, title):
    df = feature_selection_result.iloc[1:,:].pivot(index="method_name", columns="feature_num", values="selection_time")

    fig = plt.figure(figsize=(20, 5))
    ax = sns.heatmap(df, cmap="flare", annot=True, fmt=".2f", linewidths=0.5, cbar=False)
    ax.set(xlabel="Methods", ylabel="Feature Number", title=title)
    fig.savefig(address, dpi=300)

    print("Saved: {}".format(address))
    plt.close(fig)


def main():

    # Landmark plots
    print("========Landmark Feature Plots========")

    feature_selection_result = pd.read_csv("outcome/feature_selection/feature_selection_landmarks.csv")
    methods = feature_selection_result.loc[1:, "method_name"].unique().tolist()
    n_features = feature_selection_result.loc[1:, "feature_num"].unique().tolist()
    df = get_data("outcome/prev/merged_landmarks.csv")
    x_cols, y_cols = get_cols(df)
    feature_cols = [col for col in df.columns if 'norm_cenrot-' in col]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection/variance_dotplot_landmarks.png", "Variance Dotplot of All Landmark Features")
    correlation_matrix(df_X, "outcome/feature_selection/correlation_matrix_landmarks.png", "Correlation Matrix of All Landmark Features")
    landmark_plots(df, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection/method_scores_landmarks.png", "CV Scores of All Landmark Selection Methods")
    confusion_matrix(feature_selection_result, methods, False, "outcome/feature_selection")
    best_landmark_plots(df, x_cols, y_cols, feature_selection_result,"outcome/feature_selection/best_landmarks.png")
    selection_time_plot(feature_selection_result, "outcome/feature_selection/selection_time_landmarks.png", "Running Time of All Landmark Selection Methods")

    # Euclidean distance plots
    print("========Euclidean Feature Plots========")

    feature_selection_result = pd.read_csv("outcome/feature_selection/feature_selection_euclidean.csv")
    methods = feature_selection_result.loc[1:, "method_name"].unique().tolist()
    n_features = feature_selection_result.loc[1:, "feature_num"].unique().tolist()
    df = get_data("outcome/euclidean/euclidean_merged.csv")
    x_cols, y_cols = get_cols(df)
    feature_cols = [col for col in df.columns if 'dist_' in col]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection/variance_dotplot_euclidean.png", "Variance Dotplot of All Euclidean Distance Features")
    correlation_matrix(df_X, "outcome/feature_selection/correlation_matrix_euclidean.png", "Correlation Matrix of All Euclidean Distance Features")
    euclidean_plots(df, feature_cols, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection/method_scores_euclidean.png", "CV Scores of All Euclidean Distance Selection Methods")
    confusion_matrix(feature_selection_result, methods, True, "outcome/feature_selection")
    best_euclidean_plots(df, x_cols, y_cols, feature_selection_result,"outcome/feature_selection/best_euclidean.png")
    selection_time_plot(feature_selection_result, "outcome/feature_selection/selection_time_euclidean.png", "Running Time of All Euclidean Distance Selection Methods")


# Change data source to scale method results
def main_scale():

    # Landmark plots
    print("========Landmark Feature Plots (Scale Method)========")

    feature_selection_result = pd.read_csv("outcome/feature_selection_scale/feature_selection_landmarks_scale.csv")
    methods = feature_selection_result.loc[1:, "method_name"].unique().tolist()
    n_features = feature_selection_result.loc[1:, "feature_num"].unique().tolist()
    df = get_data_scale("outcome/scale/rotated_scale.csv")
    x_cols, y_cols = get_cols_scale(df)
    feature_cols = [col for col in df.columns if col.startswith("x") or col.startswith("y")]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection_scale/variance_dotplot_landmarks.png", "Variance Dotplot of All Landmark Features Using Scale Method")
    correlation_matrix(df_X, "outcome/feature_selection_scale/correlation_matrix_landmarks.png", "Correlation Matrix of All Landmark Features Using Scale Method")
    landmark_plots(df, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection_scale")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection_scale/method_scores_landmarks.png", "CV Scores of All Landmark Selection Methods Using Scale Method")
    confusion_matrix(feature_selection_result, methods, False, "outcome/feature_selection_scale")
    best_landmark_plots(df, x_cols, y_cols, feature_selection_result,"outcome/feature_selection_scale/best_landmarks.png")
    selection_time_plot(feature_selection_result, "outcome/feature_selection_scale/selection_time_landmarks.png", "Running Time of All Landmark Selection Methods Using Scale Method")

    # Euclidean distance plots
    print("========Euclidean Feature Plots (Scale Method)========")

    feature_selection_result = pd.read_csv("outcome/feature_selection_scale/feature_selection_euclidean_scale.csv")
    methods = feature_selection_result.loc[1:, "method_name"].unique().tolist()
    n_features = feature_selection_result.loc[1:, "feature_num"].unique().tolist()
    df = get_data_scale("outcome/euclidean/euclidean_merged_scale.csv")
    x_cols, y_cols = get_cols_scale(df)
    feature_cols = [col for col in df.columns if 'dist_' in col]
    df_X = df.loc[:, feature_cols]

    variance_dotplot(df_X, "outcome/feature_selection_scale/variance_dotplot_euclidean.png", "Variance Dotplot of All Euclidean Distance Features Using Scale Method")
    correlation_matrix(df_X, "outcome/feature_selection_scale/correlation_matrix_euclidean.png", "Correlation Matrix of All Euclidean Distance Features Using Scale Method")
    euclidean_plots(df, feature_cols, x_cols, y_cols, feature_selection_result, methods, "outcome/feature_selection_scale")
    method_score_plot(feature_selection_result, methods, n_features, "outcome/feature_selection_scale/method_scores_euclidean.png", "CV Scores of All Euclidean Distance Selection Methods Using Scale Method")
    confusion_matrix(feature_selection_result, methods, True, "outcome/feature_selection_scale")
    best_euclidean_plots(df, x_cols, y_cols, feature_selection_result,"outcome/feature_selection_scale/best_euclidean.png")
    selection_time_plot(feature_selection_result, "outcome/feature_selection_scale/selection_time_euclidean.png", "Running Time of All Euclidean Distance Selection Methods Using Scale Method")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scale":
        main_scale()
    else:
        main()