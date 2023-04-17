## Introduction

This documentation provides an overview of the project structure and the usage of each file. The goal is to provide
clear and concise information on the project, make the code understandable, and share our thought process for each step.


## Project Structure

#### Environment

The `Makefile` contains all the commands for the project, and all of the code is located in the `src` folder.

To set up the environment, run `conda env create -f environment.yml` and activate it
with `conda activate DS5110-faces-extend`. After that, you can run the scale functions.


#### Data Source

The original infants' and adults' landmarks data is located in the `data` folder, and it can be accessed directly by
running `make data`. Another important part of our analysis is the data from a previous project, which includes
coordinates that have been scaled and rotated. As this is not a public project, the data file is located
in `outcome/prev/merged_landmarks.csv`.


#### Makefile

The `Makefile` serves as the entry point for the entire project, and all of the completed functions are located there.
It contains four parts:

- `data`: Used for downloading the original data from Michael Wan's study.
- `scale`: Used for applying different scaling functions to the original data and comparing it with the `merged_landmarks` from the previous project.
- `outlier`: Used for detecting different functions that can be used for detecting outliers in the landmarks.
- `euclidean`: The command is used for generating euclidean distances between landmarks.
- `euclidean_scale`: Euclidean Distances generation with data source changed to `rotated_scale.csv` for comparison.
- `feature`: The command is used for feature selection method implementation. This step can be very time-consuming up to tens of minutes. Results are saved as CSV files.
- `feature_plots`: The command is used for generating feature selection related figures.
- `feature_scale`: Feature selection implementation with data source changed to `rotated_scale.csv` for comparison.
- `feature_plots_scale`: Feature selection figures with data source changed to `rotated_scale.csv` for comparison.


### Code Files

> utils.py

This file stores some common functions that are used by various scripts.

- `reshape_to_2d`: Reshapes the DataFrame into a 3d array. Data in the 3rd dimension would be (x, y) coordinates.

- `get_data`: Read CSV file from the previous program and typecast several columns to uniform formats.

- `get_data_scale`: Read CSV file from scale method part and select data from `normalized` method. Typecast several columns to uniform formats.to uniform formats.

- `get_cols`: Get x and y coordinates column name lists in the CSV file of the previous program 

- `get_cols_scale`: Get x and y coordinates column name lists in the CSV file from scale method part 


> euclidean.py

This file calculates Euclidean Distances between landmarks based on their coordinates. The `euclidean_distances` function from `sklearn.metrics.pairwise` will be used which computes the distance matrix between each pair from a vector array X and Y.

The formulas to calculate Euclidean Distances for two dimensions and higher dimensions are:

$$
\begin{align}
d(p,q) = \sqrt{(q_1-p_1)^2 + (q_2-p_2)^2} \\
d(p,q) = \sqrt{(p_1- q_1)^2 + (p_2 - q_2)^2+\cdots+(p_n - q_n)^2} \\
\end{align}
$$

- `distance_by_coordinates`: Apply `euclidean_distances` from `sklearn.metrics.pairwise` to calculate Eucidean Distances based on the reshaped 3d DataFrame. The result would be stored as a (row, 68, 68) DataFrame.

- `get_distance_cols`: Extract the Euclidean Distance data from the result of `distance_by_coordinates` and store them as a 2d DataFrame, with column names indicating the landmark pair of each distance.

- `create_euclidean_df`: Combine results of `get_distance_cols` and the original DataFrame together.

- `main`: Call`create_euclidean_df` to generate euclidean DataFrame to `merged_landmarks.csv` from the previous project. The results would be stored as `euclidean_merged.csv`.

- `main_scale`: Change data source to scale method results `rotated_scale.csv` and regenerate results in `main`. The results would be stored as `euclidean_merged_scale.csv`.


> scale.py

The `scale.py` file is used for applying scaling functions to the original data.

Before applying these scaling functions, we need to merge the data into a DataFrame with the same columns for landmarks
and other columns containing properties we care about. We add a `baby` column to mark whether the data belongs to the
baby or adult DataFrame, and we combine the image-set and filename in the infant dataset to get a similar `image_name`
in the adult dataset.

We then subtract all coordinates by the specified `x33` and `y33`, which are the coordinates of the nose. This moves all
the centers in the image to `(0,0)` in the new DataFrame. The formula is:

$$
\begin{align}
sx_i=x_i - x_{33}\\
sy_i=y_i - y_{33}\\
\end{align}
$$

After that, we rotate the image to ensure that all the images are in the same posture. This is done using the same
rotation method as in the previous project. The function is located in `rotate_calculator.py`, which will be introduced
later.

We now have three datasets: `all_raw_df`, which contains the original data; `center_by_nose_df`, which has the data
aligned to the center by the nose; and `rotated_df`, which has the data rotated to the same orientation. In the
following functions, we apply these datasets to different scaling functions. Before applying them, we would like to
introduce the scaling function used in the previous project.

The previous project had two kinds of data as a result. They combined all the data, added a `baby` column, and made the
nose the center. They then rotated the data using the same method as in `rotate_calculator.py`. After that, they scaled
the data using this formula:

$$
\begin{align}
sx_i=(x_i - x_{33})/range\\
sy_i=(y_i - y_{33})/range\\
range = (max(X \cup Y) - min(X \cup Y))\\
\end{align}
$$

This was the final set of landmarks used in all calculations.

We tried three scaling functions after center alignment and rotation:

- `standardize_original`: This function applies `StandardScaler` to the dataset. The formula is:

$$
\begin{align}
sx_i = \frac{x_i - \mu_x}{\sigma_x}\\
sy_i = \frac{y_i - \mu_y}{\sigma_y}\\
\end{align}
$$

- `normalize_by_face_bounding_box`: This function normalizes the data in a similar way to the previous project:

$$
\begin{align}
sx_i=(x_i - x_{33})/range_x\\
sy_i=(y_i - y_{33})/range_y\\
range_x = max(X) - min(X)\\
range_y = max(Y) - min(Y)\\
\end{align}
$$

- `normalize_coords_by_face_bounding_box`: This function is the actual calculation function, and the above function
  combines the results into an appropriate DataFrame.

- `scale_mds`: This function applies `mds` scaling to the landmarks.

    - `mds_by_coordinates`: This function applies `mds` scaling in the required format, and the above function
      transforms the result into an appropriate DataFrame.

- `scale_all`: This function scales the DataFrame using the three methods above, marks the scale type being used, and
  concatenates them together.

After that, we scale all the DataFrames we obtained earlier (`all_raw_df`, `center_by_nose_df`, and `rotated_df`) using
the `scale_all` function. We output these DataFrames to the `outcome/scale` folder, which is prepared for future
analysis. The mission of `scale.py` is completed.


> rotate_calculator.py

This function is used to calculate the angles and apply them to the DataFrame. The steps are:

1. **Select Landmark Groups**: Choose two groups of landmarks for rotation calculation: `[36, 45], [39, 42]` (outer and
   inner eye corners) and `[37, 44], [38, 43], [40, 47], [41, 46]` (upper and lower eyelids). These two groups are
   calculated separately. The two groups are defined in the `default_syms` variable.

2. **Calculate the Angle**: The angle is determined using the following formula:

   ```
   xx = right_x - left_x
   yy = left_y - right_y (since the y coordinate is from up to down)
   hypots = np.hypot(xx, yy)
   weight = np.sum(hypots)
   x = np.sum(xx * hypots) / weight
   y = np.sum(yy * hypots) / weight
   angle = np.arctan(y / x)
   ```

   The code for this calculation can be found in the `_get_yaw` function.

3. **Combine the Angles**:

   ```
   weights = [len(groups) for all_group]
   angle = np.sum(angles * weights) / np.sum(weights)
   ```

   The code for this calculation can be found in the `get_angle` function.

4. **Compute New Coordinates**: Calculate the new coordinates after applying the rotation:

   ```
   rotx = np.array([[cos, sin], [-sin, cos]])
   coords = coords @ rotx
   ```

   The code for this calculation can be found in the `rotate` function.


> scale_plt.py

This function is used to plot the distribution of the landmarks, obtain a visualization of them, and find some insights
from them. In the first part, we read the data from the raw file generated in `scale.py`, combine them together, and
split them into infants and adults.

The `plot` function is used to plot the DataFrame as a grid image. The columns of the grid represent the scale type, and
the rows represent some fixed indices, so we can obtain a direct understanding of the effect of each scaling method.

After that, we plot the raw data and the data that has been aligned to the center. The `plot_center` function is used to
merge the data from the previous project and the original data for comparison.

After plotting the center data, we read the rotated data and use the `plot_rotated` function to draw an image.

Finally, we obtain six images of different data and scaling methods that we used, providing us with a direct
visualization. You can find them in the `outcome/scale/` folder.


> scatter.py

The `scatter.py` file is used for plotting the boxplot and scatter plot of mean of each variable to show the
distribution of landmarks for both infants and adults.

1. Read the merged_landmarks.csv file using the pandas library to separate the data into infants and adults.

2. For each dataset, calculate the means, medians, standard deviations, and ranges of the x and y coordinates of each
   landmark.

3. Plot a scatter plot of the mean of each variable to show the distribution of landmarks.

4. Plot a boxplot of the x and y coordinates of each landmark to visualize the distribution of landmarks.


> outlier.py

The `outlier.py` file is used for performing outlier detection on face landmarks data using two methods: Mahalanobis
distance and isolation forest.

1. Read the merged_landmarks.csv file using the pandas library to separate the data into infants and adults.

2. The function of `data()` extracts the 'norm_cenrot-x{}' and 'norm_cenrot-y{}' columns from the input DataFrame and
   returns a new DataFrame with columns 'x{}' and 'y{}', where {} is an index from 0 to 67. The function then
   concatenates the columns by axis 1 and returns the resulting DataFrame.

3. The `make_noise()` function generates random data and concatenates it to the original data. The data generated has
   the same format as the original data and has 5% of the rows of the original data. The function then returns the
   modified data.

4. The `ma()` function calculates the Mahalanobis distance for the input data using the sklearn MinCovDet class. It then
   determines a threshold for outlier detection and returns the index of the outliers in the input data.

5. The `isolation()` function applies the sklearn IsolationForest class to the input data to determine the outliers. The
   function returns the index of the outliers in the input data.

6. The main() function calls the data() function to prepare the data and the make_noise() function to add noise to the
   data. It then applies the ma() and isolation() functions to the original and modified data to detect outliers.
   Finally, it prints the indices of the outliers detected for each data set and method.

> outlier_scale.py

The `outlier_scale.py` file is used for evaluating efficiency of three scaling techniques by using our two outlier
detection model on datasets obtained from these methods.

1. We first read in the dataset and separate it into three different scaling methods: standard, normalized, and MDS. We
   then extract the x and y coordinate columns and reorganize them into six different datasets for each scaling method
   and age group.

2. We then use the make_noise function to add 5% noise points to the original data for each dataset and then use the
   Mahalanobis and Isolation Forest models to detect outliers in the noisy datasets.

3. Lastly, we compare the results of the two models for each scaling technique and age group to evaluate the efficiency
   of the outlier detection models on datasets obtained from different scaling techniques.


> feature_selection.py

This file contains the entire process of feature selection and performance analytics. The selection could be slow and cost tens of minutes to complete. All feature selection and performance analytics results would be stored in CSV files for the convenience of plotting and analyzing.

- `variance_threshold`: Set a threshold to remove features with low variance. `VarianceThreshold` of `sklearn.feature_selection` was applied. Show the shape of feature matrix before and after applying threshold. 

- `correlation_threshold`: Find features with high correlation with others. Drop the feature in each pair with lower correlation with target variable. Show the shape of feature matrix after applying dropping.

- `feature_selection`: The main process of feature selection. Set 7 different selection methods (including 6 methods and 1 without selection) and 8 required feature numbers to make up 49 different selectors. The DataFrame would be firstly filtered by `variance_threshold` and `correlation_threshold`, and then be passed to different selectors in a loop. Each selector would build a model to fit and tranform the DataFrame to get required number of features. Meanwhile, the running time of each selection would be recorded and shown. 

- `feature_selection_performance`: The main process of feature selection performance analytics. Apply `LogisticRegression` to fit results of each feature selection, and record cross-validation scores. Apply `confusion_matrix` to generate confusion matrices of each feature selection. All results would be recorded in a DataFrame `feature_selection_result`.

- `main`: Apply `feature_selection` and `feature_selection_performance` to generate feature selection results for both landmark coordinates and Euclidean Distances. The data source would be `merged_landmarks.csv` from the previous project. The results would be stored in `feature_selection_landmarks.csv` and `feature_selection_euclidean.csv`.

- `main_scale`: Change data source to scale method results `rotated_scale.csv` and regenerate results in `main`. The results would be stored in `outcome/feature_seletion_scale` folder.


> feature_selection_plots.py

This file generates all feature selection related plots.

- `variance_dotplot`: Generate dot plots to show the variance distribution of features.

- `correlation_matrix`: Generate heatmaps to show the correlation between features.

- `get_mean_landmark`: Calculate the mean x and y coordinates of landmarks and their value range

- `mean_landmark_plot`: Based on results from `get_mean_landmark`, generate scatter plots to show all landmarks with mean coordinates. A horizontal line and a vertical line were drawn at x=0 and y=0.

- `landmark_feature_plot`: Generate scatter plots to show landmarks that were selected as features. Generate lines to show x and y coordinate directions.

- `landmark_plots`: Call `mean_landmark_plot` and `landmark_feature_plot` to generate plots for each feature selection method. Each method plot would contain 8 subplots, with each representing one selector.

- `get_best_selectors`: Set a criterion to select "good" selection results from `feature_selection_result`. The criterion requires a cross-validation test score above 0.88 and the feature number as few as possible.

- `best_landmark_plots`: Call `get_best_selectors` to get "good" selection results of landmarks. Call `mean_landmark_plot` and `landmark_feature_plot` to generate plots for them.

- `euclidean_feature_plot`: Generate scatter plots to show landmarks that were selected to make up distance features. Generate lines to show distances between pairs of landmarks.

- `euclidean_plots`: Call `mean_landmark_plot` and `euclidean_feature_plot` to generate plots for each feature selection method. Each method plot would contain 8 subplots, with each representing one selector.

- `best_euclidean_plots`: Call `get_best_selectors` to get "good" selection results of Euclidean Distances. Call `mean_landmark_plot` and `euclidean_feature_plot` to generate plots for them.

- `confusion_matrix`: Generate heatmaps to show confusion matrices of feature selection results. The function can be used for both landmark and Euclidean Distance results, determined by the boolean parameter.

- `method_score_plot`: Generate line plots to show all cross-validation train and test scores for all feature selection results.

- `selection_time_plot`: Generate heatmaps to show the running time for each feature selection selector.

- `main`: The `main` function would generate plots for results of landmark coordinate features stored in `feature_selection_landmarks.csv`, by calling functions `variance_dotplot`, `correlation_matrix`, `landmark_plots`, `method_score_plot`, `confusion_matrix`, `best_landmark_plots`, `selection_time_plot`. It would also generate plots for results of Euclidean Distance features stored in `feature_selection_euclidean.csv`, by calling functions `variance_dotplot`, `correlation_matrix`, `euclidean_plots`, `method_score_plot`, `confusion_matrix`, `best_euclidean_plots`, `selection_time_plot`. The results would be stored in `outcome/feature_selection` folder.

- `main_scale`: Change data source to scale method results and regenerate all plots in `main`. The results would be stored in `outcome/feature_seletion_scale` folder.


