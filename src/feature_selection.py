import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif, mutual_info_classif, SequentialFeatureSelector, RFE, SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
    

def feature_selector_pipelines():
    n_features = [5, 10, 20, 30, 40, 50]
    pipelines = {}
    feature_selectors = {}

    for enum, i in enumerate(n_features):
        # SelectKBest using f_classif
        pipeline_name = "pipeline_{}".format(enum + 1)
        selector_name = "f_classif_param_{}".format(i)
        selector_method = SelectKBest(f_classif, k=i)
        pipeline = Pipeline([
            (selector_name, selector_method),
            ("logistic_regression", LogisticRegression())
        ])
        pipelines[pipeline_name] = pipeline
        feature_selectors[pipeline_name] = (selector_name, selector_method)

        # SelectKBest using mutual_info_classif
        pipeline_name = "pipeline_{}".format(enum + 7)
        selector_name = "mutual_info_classif_param_{}".format(i)
        selector_method = SelectKBest(mutual_info_classif, k=i)
        pipeline = Pipeline([
            (selector_name, selector_method),
            ("logistic_regression", LogisticRegression())
        ])
        pipelines[pipeline_name] = pipeline
        feature_selectors[pipeline_name] = (selector_name, selector_method)
        
        # Forward Feature Selector
        pipeline_name = "pipeline_{}".format(enum + 13)
        selector_name = "sequential_feature_selector_param_{}".format(i)
        selector_method = SequentialFeatureSelector(estimator=LogisticRegression(), n_features_to_select=i, direction="forward", n_jobs=-1)
        pipeline = Pipeline([
            (selector_name, selector_method),
            ("logistic_regression", LogisticRegression())
        ])
        pipelines[pipeline_name] = pipeline
        feature_selectors[pipeline_name] = (selector_name, selector_method)

        # RFE
        pipeline_name = "pipeline_{}".format(enum + 19)
        selector_name = "rfe_param_{}".format(i)
        selector_method = RFE(estimator=LogisticRegression(), n_features_to_select=i)
        pipeline = Pipeline([
            (selector_name, selector_method),
            ("logistic_regression", LogisticRegression())
        ])
        pipelines[pipeline_name] = pipeline
        feature_selectors[pipeline_name] = (selector_name, selector_method)

        # LASSO Regularization (L1)
        pipeline_name = "pipeline_{}".format(enum + 25)
        selector_name = "lasso_regulation_param_{}".format(i)
        logistic = LogisticRegression(penalty="l1", solver="liblinear", random_state=7)
        selector_method = SelectFromModel(estimator=logistic, max_features=i)
        pipeline = Pipeline([
            (selector_name, selector_method),
            ("logistic_regression", LogisticRegression())
        ])
        pipelines[pipeline_name] = pipeline
        feature_selectors[pipeline_name] = (selector_name, selector_method)

        # Random Forest Classifier
        pipeline_name = "pipeline_{}".format(enum + 31)
        selector_name = "random_forest_classifier_param_{}".format(i)
        random_forest = RandomForestClassifier(random_state=7)
        selector_method = SelectFromModel(estimator=random_forest, max_features=i)
        pipeline = Pipeline([
            (selector_name, selector_method),
            ("logistic_regression", LogisticRegression())
        ])
        pipelines[pipeline_name] = pipeline
        feature_selectors[pipeline_name] = (selector_name, selector_method)
    
    return pipelines, feature_selectors
        

def feature_seletion(pipelines, feature_selectors, df, feature_cols):
    df_X = df.loc[:, X_cols]
    X = df_X.values
    y = df.loc[:, "baby"].values
    print("Shape of feature matrix: {}.".format(X.shape))

    # Remove features with low variance
    method = VarianceThreshold()
    method.fit(X, y)
    mask = method.get_support()

    X_cols_new = df_X.columns[mask]
    df_X_new = df.loc[:, X_cols_new]
    X_new = df_X_new.values
    print("Shape of feature matrix after remove low variance features: {}.".format(X_new.shape))

    for i in range(1, 37):
        pipeline_name = "pipeline_{}".format(i)
        pipeline = pipelines[pipeline_name]
        selector_name, selector_method = feature_selectors[pipeline_name]

        print("Feature Selector: ", selector_name)

        selector_method.fit(X_new, y)
        feature_mask = selector_method.get_support()
        feature_names = df_X_new.columns[feature_mask]
        print("Selected Features: ", list(feature_names))

        pipeline.fit(X_new, y)
        scores = cross_validate(pipeline, X_new, y, cv=5, return_train_score=True)
        print("Cross Validation Train Score: {:.2e} +/- {:.2e}.".format(scores["train_score"].mean(), scores["train_score"].std()))
        print("Cross Validation Test Score: {:.2e} +/- {:.2e}.".format(scores["test_score"].mean(), scores["test_score"].std()))


def main():
    df = pd.read_csv("outcome/prev/merged_landmarks.csv")
    feature_cols = [col for col in df.columns if 'norm_cenrot-' in col]
    pipelines, feature_selectors = feature_selector_pipelines()
    feature_seletion(pipelines, feature_selectors, df, feature_cols)


if __name__ == '__main__':
    main()

