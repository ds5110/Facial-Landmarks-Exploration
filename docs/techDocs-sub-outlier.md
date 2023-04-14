##### scale.py

The `scatter.py` file is used for plotting the boxplot and scatter plot of mean of each variable to show the distribution of landmarks for both infants and adults.

1. Read the merged_landmarks.csv file using the pandas library to separate the data into infants and adults.

2. For each dataset, calculate the means, medians, standard deviations, and ranges of the x and y coordinates of each landmark.

3. Plot a scatter plot of the mean of each variable to show the distribution of landmarks.

4. Plot a boxplot of the x and y coordinates of each landmark to visualize the distribution of landmarks.

##### outlier_new.py

The `outlier_new.py` file is used for performing outlier detection on face landmarks data using two methods: Mahalanobis distance and isolation forest. 

1. Read the merged_landmarks.csv file using the pandas library to separate the data into infants and adults.

2. The function of `data()` extracts the 'norm_cenrot-x{}' and 'norm_cenrot-y{}' columns from the input data frame and returns a new data frame with columns 'x{}' and 'y{}', where {} is an index from 0 to 67. The function then concatenates the columns by axis 1 and returns the resulting data frame.

3. The `make_noise()` function generates random data and concatenates it to the original data. The data generated has the same format as the original data and has 5% of the rows of the original data. The function then returns the modified data.

4. The `ma()` function calculates the Mahalanobis distance for the input data using the sklearn MinCovDet class. It then determines a threshold for outlier detection and returns the index of the outliers in the input data.

5. The `isolation()` function applies the sklearn IsolationForest class to the input data to determine the outliers. The function returns the index of the outliers in the input data.

6. The main() function calls the data() function to prepare the data and the make_noise() function to add noise to the data. It then applies the ma() and isolation() functions to the original and modified data to detect outliers. Finally, it prints the indices of the outliers detected for each data set and method.

##### outlier_new_scale.py

The `outlier_new_scale.py` file is used for evaluating efficiency of three scaling techniques by using our two outlier detection model on datasets obtained from these methods.

1. We first read in the dataset and separate it into three different scaling methods: standard, normalized, and MDS. We then extract the x and y coordinate columns and reorganize them into six different datasets for each scaling method and age group.

2. We then use the make_noise function to add 5% noise points to the original data for each dataset and then use the Mahalanobis and Isolation Forest models to detect outliers in the noisy datasets.

3. Lastly, we compare the results of the two models for each scaling technique and age group to evaluate the efficiency of the outlier detection models on datasets obtained from different scaling techniques.





