import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif, mutual_info_classif, SequentialFeatureSelector, RFE, SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix
import time
from utils import get_data, get_data_scale


# Remove features with low variance    
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


# Remove features with high correlation with others
# Drop the feature in the pair with lower correlation with target
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

# Six different feature selection methods as well as all features
def feature_selection(df, feature_cols):
    methods = ["all_features",
               "f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regulation", 
               "random_forest_classifier"]
    n_features = [2, 3, 5, 10, 15, 20, 25, 30]
    feature_names = {}
    df_X_after_vt, df_y, y = variance_threshold(df, feature_cols, threshold=0.0005)
    df_X_after_ct, X_after_ct = correlation_threshold(df_X_after_vt, df_y, threshold=0.95)
    
    # All features
    selector_name = methods[0]
    feature_names[selector_name] = df_X_after_ct.columns
    
    for i in n_features:
        ts_before = time.time()
        print(f"Feature Selection for {i} features...", end="", flush=True)

        # SelectKBest using f_classif
        selector_name = "{}_num_{}".format(methods[1], i)
        selector_method = SelectKBest(f_classif, k=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        # SelectKBest using mutual_info_classif
        selector_name = "{}_num_{}".format(methods[2], i)
        selector_method = SelectKBest(mutual_info_classif, k=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]
        
        # Forward Feature Selector
        selector_name = "{}_num_{}".format(methods[3], i)
        selector_method = SequentialFeatureSelector(estimator=LogisticRegression(random_state=7, max_iter=10000), n_features_to_select=i, direction="forward", n_jobs=-1)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        # RFE
        selector_name = "{}_num_{}".format(methods[4], i)
        selector_method = RFE(estimator=LogisticRegression(random_state=7, max_iter=10000), n_features_to_select=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        # LASSO Regularization (L1)
        selector_name = "{}_num_{}".format(methods[5], i)
        logistic = LogisticRegression(penalty="l1", solver="liblinear", random_state=7, max_iter=10000)
        selector_method = SelectFromModel(estimator=logistic, max_features=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        # Random Forest Classifier
        selector_name = "{}_num_{}".format(methods[6], i)
        random_forest = RandomForestClassifier(random_state=7, n_jobs=-1)
        selector_method = SelectFromModel(estimator=random_forest, max_features=i)
        selector_method.fit(X_after_ct, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_after_ct.columns[feature_mask]

        ts_after = time.time()
        print("done. [{:.2f} seconds]".format(ts_after - ts_before))
    
    return feature_names
        

# Test selected features using logistic regression
def feature_seletion_performance(feature_names, df, feature_cols):
    y = df.loc[:, "baby"].values
    column_names = ["selector_name",
                    "CV_train_score_mean",
                    "CV_train_score_std",
                    "CV_test_score_mean",
                    "CV_test_score_mean",
                    "CM_true_adult",
                    "CM_false_infant",
                    "CM_false_adult",
                    "CM_true_infant"] + feature_cols
    feature_selection_result = pd.DataFrame(index=range(49), columns=column_names)

    ts_before = time.time()
    print("Test feature selection performance...", end="")
    for i in range(49):
        selector_name = list(feature_names.keys())[i]
        selected_features = list(feature_names.values())[i]
        df_X_selected = df.loc[:, selected_features]
        X_selected = df_X_selected.values

        feature_selection_result.iloc[i, 0] = selector_name
        logistic = LogisticRegression(random_state=7, max_iter=10000)
        logistic.fit(X_selected, y)
        scores = cross_validate(logistic, X_selected, y, cv=5, return_train_score=True)
        
        feature_selection_result.iloc[i, 1] = scores["train_score"].mean()
        feature_selection_result.iloc[i, 2] = scores["train_score"].std()
        feature_selection_result.iloc[i, 3] = scores["test_score"].mean()
        feature_selection_result.iloc[i, 4] = scores["test_score"].std()

        y_pred = cross_val_predict(logistic, X_selected, y, cv=5)
        cm = confusion_matrix(y, y_pred, labels=[0, 1])
        feature_selection_result.iloc[i, 5:9] = cm.flatten().tolist()

        feature_selection_result.iloc[i, 9:] = [feature_col in selected_features for feature_col in feature_cols]

    ts_after = time.time()
    print("done. [{:.2f} seconds]".format(ts_after - ts_before))

    return feature_selection_result
    

def main():

    # landmark coordinates as features
    print("========Landmark Feature Selection========")

    df = get_data("outcome/prev/merged_landmarks.csv")
    feature_cols = [col for col in df.columns if "norm_cenrot-" in col]

    feature_names = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols)
    
    address = "outcome/feature_selection/feature_selection_landmarks.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of landmarks has been saved as '{}'.".format(address))
    
    # euclidean distances as features
    print("========Euclidean Distance Feature Selection========")

    df = get_data("outcome/euclidean/euclidean_merged.csv")
    feature_cols = [col for col in df.columns if "dist_" in col]

    feature_names = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols)
    
    address = "outcome/feature_selection/feature_selection_euclidean.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of euclidean distances has been saved as '{}'.".format(address))


def main_scale():

    # landmark coordinates as features
    print("========Landmark Feature Selection (Scale Method)========")

    df = get_data_scale("outcome/scale/rotated_scale.csv")
    feature_cols = [col for col in df.columns if col.startswith("x") or col.startswith("y")]

    feature_names = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols)
    
    address = "outcome/feature_selection_scale/feature_selection_landmarks.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of landmarks using scale method has been saved as '{}'.".format(address))
    
    # euclidean distances as features
    print("========Euclidean Feature Selection (Scale Method)========")

    df = get_data_scale("outcome/euclidean/euclidean_merged_scale.csv")
    feature_cols = [col for col in df.columns if "dist_" in col]

    feature_names = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols)
    
    address = "outcome/feature_selection_scale/feature_selection_euclidean.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of euclidean distances using scale method has been saved as '{}'.".format(address))


if __name__ == "__main__":
    main()
    # main_scale()

