import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif, mutual_info_classif, SequentialFeatureSelector, RFE, SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix


# Remove features with low variance    
def variance_threshold(df, feature_cols):
    df_X = df.loc[:, feature_cols]
    X = df_X.values
    y = df.loc[:, "baby"].values

    method = VarianceThreshold()
    method.fit(X, y)
    mask = method.get_support()

    X_cols_new = df_X.columns[mask]
    df_X_new = df.loc[:, X_cols_new]
    X_new = df_X_new.values

    return df_X_new, X_new, y


# Six different feature selection methods as well as all features
def feature_selection(df, feature_cols):
    methods = ["all_features",
               "f_classif", 
               "mutual_info_classif", 
               "sequential_feature_selector", 
               "rfe", 
               "lasso_regulation", 
               "random_forest_classifier"]
    n_features = [2, 3, 5, 10, 15, 20, 30, 50]
    feature_names = {}
    df_X_new, X_new, y = variance_threshold(df, feature_cols)

    # All features
    selector_name = methods[0]
    feature_names[selector_name] = df_X_new.columns

    for i in n_features:
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
        selector_method = SequentialFeatureSelector(estimator=LogisticRegression(), n_features_to_select=i, direction="forward", n_jobs=-1)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        # RFE
        selector_name = "{}_num_{}".format(methods[4], i)
        selector_method = RFE(estimator=LogisticRegression(), n_features_to_select=i)
        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names[selector_name] = df_X_new.columns[feature_mask]

        # LASSO Regularization (L1)
        selector_name = "{}_num_{}".format(methods[5], i)
        logistic = LogisticRegression(penalty="l1", solver="liblinear", random_state=7)
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
    
    return feature_names
        

# Test selected features using logistic regression
def feature_seletion_performance(feature_names, df, feature_cols):
    df_X_new, X_new, y = variance_threshold(df, feature_cols)
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

    for i in range(49):
        selector_name = list(feature_names.keys())[i]
        selected_features = list(feature_names.values())[i]
        df_X_selected = df_X_new.loc[:, selected_features]
        X_selected = df_X_selected.values

        feature_selection_result.iloc[i, 0] = selector_name
        logistic = LogisticRegression(random_state=7)
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

    return feature_selection_result


def main():
    df = pd.read_csv("outcome/prev/merged_landmarks.csv")
    feature_cols = [col for col in df.columns if "norm_cenrot-" in col]

    feature_names = feature_selection(df, feature_cols)
    feature_selection_result = feature_seletion_performance(feature_names, df, feature_cols)
    feature_selection_result.to_csv('outcome/feature_selection/feature_selection.csv', index=False)


if __name__ == "__main__":
    main()

