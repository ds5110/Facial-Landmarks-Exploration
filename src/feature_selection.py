import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif, mutual_info_classif, SequentialFeatureSelector, RFE, SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix
import time
from utils import get_data


# Remove features with low variance    
def variance_threshold(df, feature_cols, threshold):
    df_X = df.loc[:, feature_cols]
    X = df_X.values
    y = df.loc[:, "baby"].values
    print("Original shape of feature matrix: {}".format(X.shape))

    method = VarianceThreshold(threshold=threshold)
    method.fit(X)
    mask = method.get_support()

    X_cols_new = df_X.columns[mask]
    df_X_new = df.loc[:, X_cols_new]
    X_new = df_X_new.values
    print("Shape of feature matrix after variance threshold: {}".format(X_new.shape))

    return df_X_new, X_new, y


# Six different feature selection methods as well as all features
def feature_selection(df, feature_cols, threshold):
    methods = ["all_features",
               "f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regulation", 
               "random_forest_classifier"]
    n_features = [2, 3, 5, 10, 15, 20, 30, 50]
    feature_names = {}
    df_X_new, X_new, y = variance_threshold(df, feature_cols, threshold=threshold)

    # All features
    selector_name = methods[0]
    feature_names[selector_name] = df_X_new.columns
    
    for i in n_features:
        ts_before = time.time()
        print(f"Feature Selection for {i} features...", end="", flush=True)

        # SelectKBest using f_classif
        selector_name = "{}_num_{}".format(methods[1], i)
        selector_method = SelectKBest(f_classif, k=i)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        # SelectKBest using mutual_info_classif
        selector_name = "{}_num_{}".format(methods[2], i)
        selector_method = SelectKBest(mutual_info_classif, k=i)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]
        
        # Forward Feature Selector
        selector_name = "{}_num_{}".format(methods[3], i)
        selector_method = SequentialFeatureSelector(estimator=LogisticRegression(random_state=7, max_iter=10000), n_features_to_select=i, direction="forward", n_jobs=-1)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        # RFE
        selector_name = "{}_num_{}".format(methods[4], i)
        selector_method = RFE(estimator=LogisticRegression(random_state=7, max_iter=10000), n_features_to_select=i)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        # LASSO Regularization (L1)
        selector_name = "{}_num_{}".format(methods[5], i)
        logistic = LogisticRegression(penalty="l1", solver="liblinear", random_state=7, max_iter=10000)
        selector_method = SelectFromModel(estimator=logistic, max_features=i)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        # Random Forest Classifier
        selector_name = "{}_num_{}".format(methods[6], i)
        random_forest = RandomForestClassifier(random_state=7, n_jobs=-1)
        selector_method = SelectFromModel(estimator=random_forest, max_features=i)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        ts_after = time.time()
        print("done. [{:.2f} seconds]".format(ts_after - ts_before))
    
    return feature_names
        

# Test selected features using logistic regression
def feature_seletion_performance(feature_names, df, feature_cols, threshold):
    df_X_new, X_new, y = variance_threshold(df, feature_cols, threshold=threshold)
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
        df_X_selected = df_X_new.loc[:, selected_features]
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


# def concat_normalized_df(normalized_infant, normalized_adult):
#     infant_cols, infant_x_cols, infant_y_cols = utils.get_infant_cols(normalized_infant)
#     adult_cols, adult_x_cols, adult_y_cols = utils.get_adult_cols(normalized_adult)
    
#     num_rows_infant = normalized_infant.shape[0]
#     num_rows_adult = normalized_adult.shape[0]

#     infant_image_name = pd.DataFrame({"image_name": normalized_infant["image-set"].str.cat(normalized_infant["filename"], sep="/")})
#     infant_new = pd.concat([infant_image_name, normalized_infant.loc[:, infant_cols], pd.DataFrame({"baby": [1] * num_rows_infant}, index=range(num_rows_infant))], axis=1)
#     adult_new = pd.concat([normalized_adult.iloc[:, 0], normalized_adult.loc[:, adult_cols], pd.DataFrame({"baby": [0] * num_rows_adult}, index=range(num_rows_adult))], axis=1)
#     adult_new.columns = infant_new.columns
#     normalized_all = pd.concat([infant_new, adult_new], axis=0, ignore_index=True)
    
#     return normalized_all
    

def main():
    # Concat normalized landmark data
    # normalized_infant = pd.read_csv("outcome/scale/normalized_infant.csv")
    # normalized_adult = pd.read_csv("outcome/scale/normalized_adult.csv")
    # normalized_all = concat_normalized_df(normalized_infant, normalized_adult)
    # normalized_all.to_csv("outcome/scale/normalized_all.csv", index=False)

    # landmark coordinates as features
    df = get_data("outcome/prev/merged_landmarks.csv")
    feature_cols = [col for col in df.columns if "norm_cenrot-" in col]

    threshold = 0.001
    feature_names = feature_selection(df, feature_cols, threshold=threshold)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols, threshold=threshold)
    
    address = "outcome/feature_selection/feature_selection_landmarks.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of landmarks has been saved as {}.".format(address))
    
    # euclidean distances as features
    df = get_data("outcome/euclidean/euclidean_merged.csv")
    feature_cols = [col for col in df.columns if "dist_" in col]

    threshold = 0.003
    feature_names = feature_selection(df, feature_cols, threshold=threshold)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols, threshold=threshold)
    
    address = "outcome/feature_selection/feature_selection_euclidean.csv"
    feature_selection_result.to_csv(address, index=False)
    print("Feature selection result of euclidean distances has been saved as {}.".format(address))


if __name__ == "__main__":
    main()

