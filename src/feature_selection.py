import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif, mutual_info_classif, SequentialFeatureSelector, RFE, SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix
import time
import sys
from utils import get_data, get_data_scale


# Set a threshold to remove features with low variance
def variance_threshold(df, feature_cols, threshold):
    df_X = df.loc[:, feature_cols]
    X = df_X.values
    df_y = df.loc[:, "baby"]
    y = df_y.values
    print("Original shape of feature matrix: {}".format(X.shape))

    method = VarianceThreshold(threshold=threshold)
    method.fit(X)
    mask = method.get_support()

    X_cols_after_vt = df_X.columns[mask]
    df_X_after_vt = df.loc[:, X_cols_after_vt]
    X_after_vt = df_X_after_vt.values
    print("Shape of feature matrix after variance threshold: {}".format(X_after_vt.shape))

    return df_X_after_vt, df_y, y


# Find features with high correlation with others
# Drop the feature in each pair with lower correlation with target variable
def correlation_threshold(df_X, df_y, threshold):
    corr = df_X.corr().abs()
    high_corr_features = [column for column in corr.columns if any(corr[column] > 0.5)]
    corr_with_target = df_X.corrwith(df_y).abs()

    for feature in high_corr_features:
        feature_pairs = corr.loc[:, feature].sort_values(ascending=False)
        for i in range(len(feature_pairs)):
            if feature_pairs.iloc[i] > threshold and corr_with_target[feature_pairs.index[i]] < corr_with_target[feature]:  
                df_X.drop(columns=[feature_pairs.index[i]], inplace=True, errors="ignore")
    
    df_X_after_ct = df_X
    X_after_ct = df_X_after_ct.values
    print("Shape of feature matrix after correlation threshold: {}".format(X_after_ct.shape))
    
    return df_X_after_ct, X_after_ct



# Main process of feature selection
# Seleted feature names and running time would be stored
def feature_selection(df, feature_cols):
    methods = ["all_features",
               "f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regularization", 
               "random_forest_classifier"]
    n_features = [2, 3, 5, 10, 15, 20, 25, 30]
    feature_names = {}
    selection_time = {}
    df_X_after_vt, df_y, y = variance_threshold(df, feature_cols, threshold=0.0005)
    df_X_after_ct, X_after_ct = correlation_threshold(df_X_after_vt, df_y, threshold=0.95)
    
    # All features
    selector_name =  "{}_num_{}".format(methods[0], df_X_after_ct.shape[1])
    feature_names[selector_name] = df_X_after_ct.columns
    selection_time[selector_name] = 0
    
    for i in n_features:

        # SelectKBest using f_classif
        ts_before = time.time()
        print(f"Feature selection using {methods[1]} for {i} features...", end="", flush=True)
        
        selector_name = "{}_num_{}".format(methods[1], i)
        selector_method = SelectKBest(f_classif, k=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        ts_after = time.time()
        selection_time[selector_name] = ts_after - ts_before
        print("done. [{:.2f} seconds]".format(ts_after - ts_before), flush=True)

        # SelectKBest using mutual_info_classif
        ts_before = time.time()
        print(f"Feature selection using {methods[2]} for {i} features...", end="", flush=True)

        selector_name = "{}_num_{}".format(methods[2], i)
        selector_method = SelectKBest(mutual_info_classif, k=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]
        
        ts_after = time.time()
        selection_time[selector_name] = ts_after - ts_before
        print("done. [{:.2f} seconds]".format(ts_after - ts_before), flush=True)

        # Forward Feature Selector
        ts_before = time.time()
        print(f"Feature selection using {methods[3]} for {i} features...", end="", flush=True)

        selector_name = "{}_num_{}".format(methods[3], i)
        selector_method = SequentialFeatureSelector(estimator=LogisticRegression(random_state=7, max_iter=10000), n_features_to_select=i, direction="forward", n_jobs=-1)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        ts_after = time.time()
        selection_time[selector_name] = ts_after - ts_before
        print("done. [{:.2f} seconds]".format(ts_after - ts_before), flush=True)

        # RFE
        ts_before = time.time()
        print(f"Feature selection using {methods[4]} for {i} features...", end="", flush=True)

        selector_name = "{}_num_{}".format(methods[4], i)
        selector_method = RFE(estimator=LogisticRegression(random_state=7, max_iter=10000), n_features_to_select=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        ts_after = time.time()
        selection_time[selector_name] = ts_after - ts_before
        print("done. [{:.2f} seconds]".format(ts_after - ts_before), flush=True)

        # LASSO Regularization (L1)
        ts_before = time.time()
        print(f"Feature selection using {methods[5]} for {i} features...", end="", flush=True)

        selector_name = "{}_num_{}".format(methods[5], i)
        logistic = LogisticRegression(penalty="l1", solver="liblinear", random_state=7, max_iter=10000)
        selector_method = SelectFromModel(estimator=logistic, max_features=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        ts_after = time.time()
        selection_time[selector_name] = ts_after - ts_before
        print("done. [{:.2f} seconds]".format(ts_after - ts_before), flush=True)

        # Random Forest Classifier
        ts_before = time.time()
        print(f"Feature selection using {methods[6]} for {i} features...", end="", flush=True)

        selector_name = "{}_num_{}".format(methods[6], i)
        random_forest = RandomForestClassifier(random_state=7, n_jobs=-1)
        selector_method = SelectFromModel(estimator=random_forest, max_features=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        ts_after = time.time()
        selection_time[selector_name] = ts_after - ts_before
        print("done. [{:.2f} seconds]".format(ts_after - ts_before), flush=True)
    
    return feature_names, selection_time
        

# Main process of feature selection performance analytics
def feature_seletion_performance(feature_names, selection_time, df, feature_cols):
    y = df.loc[:, "baby"].values

    # Initialize DataFrame to store all results
    column_names = ["selector_name",
                    "method_name",
                    "feature_num",
                    "CV_train_score_mean",
                    "CV_train_score_std",
                    "CV_test_score_mean",
                    "CV_test_score_mean",
                    "CM_true_adult",
                    "CM_false_infant",
                    "CM_false_adult",
                    "CM_true_infant",
                    "selection_time"] + feature_cols
    feature_selection_result = pd.DataFrame(index=range(49), columns=column_names)

    ts_before = time.time()
    print("Test feature selection performance...", end="")
    for i in range(49):
        selector_name = list(feature_names.keys())[i]
        method_name = selector_name.split("_num_")[0]
        feature_num = selector_name.split("_num_")[1]
        selected_features = list(feature_names.values())[i]
        df_X_selected = df.loc[:, selected_features]
        X_selected = df_X_selected.values

        feature_selection_result.iloc[i, 0] = selector_name
        feature_selection_result.iloc[i, 1] = method_name
        feature_selection_result.iloc[i, 2] = feature_num

        # Apply logistic regression to fit and report performance
        logistic = LogisticRegression(random_state=7, max_iter=10000)
        logistic.fit(X_selected, y)
        scores = cross_validate(logistic, X_selected, y, cv=5, return_train_score=True)
        
        feature_selection_result.iloc[i, 3] = scores["train_score"].mean()
        feature_selection_result.iloc[i, 4] = scores["train_score"].std()
        feature_selection_result.iloc[i, 5] = scores["test_score"].mean()
        feature_selection_result.iloc[i, 6] = scores["test_score"].std()

        # Generate confusion matrix results for each feature selection result
        y_pred = cross_val_predict(logistic, X_selected, y, cv=5)
        cm = confusion_matrix(y, y_pred, labels=[0, 1])
        feature_selection_result.iloc[i, 7:11] = cm.flatten().tolist()

        feature_selection_result.iloc[i, 11] = selection_time[selector_name]
        feature_selection_result.iloc[i, 12:] = [feature_col in selected_features for feature_col in feature_cols]
         

    ts_after = time.time()
    print("done. [{:.2f} seconds]".format(ts_after - ts_before))

    return feature_selection_result
    

def main():

    # landmark coordinates as features
    print("========Landmark Feature Selection========")

    df = get_data("outcome/prev/merged_landmarks.csv")
    feature_cols = [col for col in df.columns if "norm_cenrot-" in col]

    feature_names, selection_time = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, selection_time, df, feature_cols)
    
    address = "outcome/feature_selection/feature_selection_landmarks.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of landmarks has been saved as '{}'.".format(address))
    
    # euclidean distances as features
    print("========Euclidean Distance Feature Selection========")

    df = get_data("outcome/euclidean/euclidean_merged.csv")
    feature_cols = [col for col in df.columns if "dist_" in col]

    feature_names, selection_time = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, selection_time, df, feature_cols)
    
    address = "outcome/feature_selection/feature_selection_euclidean.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of euclidean distances has been saved as '{}'.".format(address))


def main_scale():

    # landmark coordinates as features
    print("========Landmark Feature Selection (Scale Method)========")

    df = get_data_scale("outcome/scale/rotated_scale.csv")
    feature_cols = [col for col in df.columns if col.startswith("x") or col.startswith("y")]

    feature_names, selection_time = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, selection_time, df, feature_cols)
    
    address = "outcome/feature_selection_scale/feature_selection_landmarks_scale.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of landmarks using scale method has been saved as '{}'.".format(address))
    
    # euclidean distances as features
    print("========Euclidean Feature Selection (Scale Method)========")

    df = get_data_scale("outcome/euclidean/euclidean_merged_scale.csv")
    feature_cols = [col for col in df.columns if "dist_" in col]

    feature_names, selection_time = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, selection_time, df, feature_cols)
    
    address = "outcome/feature_selection_scale/feature_selection_euclidean_scale.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of euclidean distances using scale method has been saved as '{}'.".format(address))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scale":
        main_scale()
    else:
        main()

