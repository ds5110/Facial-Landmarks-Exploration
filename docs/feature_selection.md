# Feature Selection

## Methods in Previous Project

**SVC**

- `PCA` to all landmark coordinates
- Manually select `boxratio` and `interoc_norm`

**Logistic Regression**

- Manually select `boxratio`
- `Forward Feature Selection` to all euclidean distances
- Combine `boxratio` and results in the 2nd step

**Bayes**

- `LDA`, `QDA`, `Gaussian Naive Bayes` to all landmark coordinates

## Data Source and Preprocessing

## Feature Selection Results (Landmarks)

### Variance Threshold

![](../outcome/feature_selection/variance_dotplot_landmarks.png)

### Correlation Threshold

![](../outcome/feature_selection/correlation_matrix_landmarks.png)

### Filter Methods

Filter methods use statistical measures to rank the features according to their relevance to the target variable. Examples of filter methods include `correlation-based feature selection`, `mutual information-based feature selection`, and `chi-squared feature selection`.

**Fisher's Score**

![](../outcome/feature_selection/confusion_matrix_landmarks_f_classif.png)

![](../outcome/feature_selection/landmarks_f_classif.png)

**Information Gain**

![](../outcome/feature_selection/confusion_matrix_landmarks_mutual_info_classif.png)

![](../outcome/feature_selection/landmarks_mutual_info_classif.png)

### Wrapper methods

Wrapper methods use a specific learning algorithm to evaluate the usefulness of subsets of features. Examples of wrapper methods include `recursive feature elimination`, `forward selection`, and `backward elimination`.

**Forward Feature Selection**

![](../outcome/feature_selection/confusion_matrix_landmarks_sequential_feature_selector.png)

![](../outcome/feature_selection/landmarks_sequential_feature_selector.png)

**Recursive Feature Elimination**

![](../outcome/feature_selection/confusion_matrix_landmarks_rfe.png)

![](../outcome/feature_selection/landmarks_rfe.png)

### Regularization methods

Regularization methods add a penalty term to the objective function that encourages sparse solutions, i.e., solutions with fewer non-zero coefficients. Examples of regularization methods include `L1 regularization (Lasso)` and `L2 regularization (Ridge Regression)`.

**L1 Regularization (Lasso)**

![](../outcome/feature_selection/confusion_matrix_landmarks_lasso_regulation.png)

![](../outcome/feature_selection/landmarks_lasso_regulation.png)

### Tree-based methods

Tree-based methods like `Random Forest` and `Gradient Boosting` can be used to rank the importance of features based on how much they contribute to the reduction in impurity or error in the decision trees.

**Random Forests**

![](../outcome/feature_selection/confusion_matrix_landmarks_random_forest_classifier.png)

![](../outcome/feature_selection/landmarks_random_forest_classifier.png)

### Conclusion

![](../outcome/feature_selection/method_scores_landmarks.png)

## Feature Selection Results (Euclidean Distances)

### Variance Threshold

![](../outcome/feature_selection/variance_dotplot_euclidean.png)

### Correlation Threshold

![](../outcome/feature_selection/correlation_matrix_euclidean.png)

### Fisher's Score

![](../outcome/feature_selection/confusion_matrix_euclidean_f_classif.png)

![](../outcome/feature_selection/euclidean_f_classif.png)

### Information Gain

![](../outcome/feature_selection/confusion_matrix_euclidean_mutual_info_classif.png)

![](../outcome/feature_selection/euclidean_mutual_info_classif.png)

### Forward Feature Selection 

![](../outcome/feature_selection/confusion_matrix_euclidean_sequential_feature_selector.png)

![](../outcome/feature_selection/euclidean_sequential_feature_selector.png)

### Recursive Feature Elimination

![](../outcome/feature_selection/confusion_matrix_euclidean_rfe.png)

![](../outcome/feature_selection/euclidean_rfe.png)

### LASSO Regularization

![](../outcome/feature_selection/confusion_matrix_euclidean_lasso_regulation.png)

![](../outcome/feature_selection/euclidean_lasso_regulation.png)

### Random Forests

![](../outcome/feature_selection/confusion_matrix_euclidean_random_forest_classifier.png)

![](../outcome/feature_selection/euclidean_random_forest_classifier.png)

### Conclusion

![](../outcome/feature_selection/method_scores_euclidean.png)







