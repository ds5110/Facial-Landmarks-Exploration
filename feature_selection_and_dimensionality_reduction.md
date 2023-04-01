# Feature Selection And Dimensionality Reduction

**feature selection methods**

- Filter methods

Filter methods use statistical measures to rank the features according to their relevance to the target variable. Examples of filter methods include `correlation-based feature selection`, `mutual information-based feature selection`, and `chi-squared feature selection`.

- Wrapper methods

Wrapper methods use a specific learning algorithm to evaluate the usefulness of subsets of features. Examples of wrapper methods include `recursive feature elimination`, `forward selection`, and `backward elimination`.

- Embedded methods

Embedded methods incorporate feature selection as part of the learning process. Examples of embedded methods include `LASSO` (Least Absolute Shrinkage and Selection Operator), `Ridge Regression`, and `Elastic Net`.

- Regularization methods

Regularization methods add a penalty term to the objective function that encourages sparse solutions, i.e., solutions with fewer non-zero coefficients. Examples of regularization methods include `L1 regularization (Lasso`) and `L2 regularization (Ridge Regression`).

- Tree-based methods

Tree-based methods like `Random Forest` and `Gradient Boosting` can be used to rank the importance of features based on how much they contribute to the reduction in impurity or error in the decision trees.

**Dimensionality Reduction Methods**

- Linear Dimensionality Reduction Methods

These methods aim to reduce the dimensionality of the data by projecting it onto a lower-dimensional space using linear transformations.

a) `Principal Component Analysis (PCA)`: PCA is a commonly used linear dimensionality reduction method that projects the data onto a new set of orthogonal axes (called principal components) that capture the maximum variance in the data.

b) `Linear Discriminant Analysis (LDA)`: LDA is another linear dimensionality reduction method that is used for classification problems. LDA finds the linear combination of features that maximizes the separation between classes while minimizing the within-class variance.

- Nonlinear Dimensionality Reduction Methods

These methods are used when the data cannot be easily represented in a lower-dimensional linear space.

a) `t-Distributed Stochastic Neighbor Embedding (t-SNE)`: t-SNE is a popular nonlinear dimensionality reduction method that maps high-dimensional data into a lower-dimensional space while preserving the pairwise similarities between data points.

b) `Autoencoders`: Autoencoders are neural network-based architectures that are trained to reconstruct the input data from a lower-dimensional latent space representation. The encoder part of the network maps the input data to the lower-dimensional space, while the decoder part reconstructs the original data from the lower-dimensional representation.

c) `Kernel PCA`: Kernel PCA is a nonlinear version of PCA that uses kernel functions to map the data into a higher-dimensional feature space, where linear PCA can be applied.

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

## Potential Features

### Landmark Coordinates

### Landmark Euclidean Distances

### Geometric Features

## Compare Selection Methods

## 