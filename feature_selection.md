# Feature Selection

## Methods in Previous Project

**SVC**

1. `PCA` to all landmark coordinates
2. no methods to "boxratio" and "interoc_norm"

**Logistic Regression**

1. no methods to "boxratio"
2. `forward feature selection` to all euclidean distances
3. combine "boxratio" and results in the 2nd step together

**bayes**

`LDA`, `QDA`, `Gaussian Naive Bayes` to all landmark coordinates

## Feature Selection Methods

**Filter methods**

Filter methods use statistical measures to rank the features according to their relevance to the target variable. Examples of filter methods include `correlation-based feature selection`, `mutual information-based feature selection`, and `chi-squared feature selection`.

**Wrapper methods**

Wrapper methods use a specific learning algorithm to evaluate the usefulness of subsets of features. Examples of wrapper methods include `recursive feature elimination`, `forward selection`, and `backward elimination`.

**Embedded methods**

Embedded methods incorporate feature selection as part of the learning process. Examples of embedded methods include `LASSO` (Least Absolute Shrinkage and Selection Operator), `Ridge Regression`, and `Elastic Net`.

**Regularization methods**

Regularization methods add a penalty term to the objective function that encourages sparse solutions, i.e., solutions with fewer non-zero coefficients. Examples of regularization methods include `L1 regularization (Lasso`) and `L2 regularization (Ridge Regression`).

**Tree-based methods**

Tree-based methods like `Random Forest` and `Gradient Boosting` can be used to rank the importance of features based on how much they contribute to the reduction in impurity or error in the decision trees.

## Potential Features

## Compare Selection Methods

## 