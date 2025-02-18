# Goals

The goal of this project is to preprocess image landmark data, analyze the relationship between the landmark data and face attributes, and help improve accuracy and efficiency in potential applications of face recognition and expression recognition.

**Expected Outcomes:**

The proposed program is expected to achieve the following outcomes:

- A recommended scaling method for the landmark data.
- An identified set of outliers to remove from the data.
- Regression and distribution analyses of Euclidean distances between landmark points, which may provide useful insights.
- A rotation method including choosing the center point and rotation axis.
- Identification of landmark differences between different types of faces (turned, tilted, occluded, and expressive), which could aid in developing a computer algorithm for identifying these types of faces.

# Data

- [InfAnFace dataset](https://coe.northeastern.edu/Research/AClab/InfAnFace/)
- [300-W](https://github.com/ostadabbas/Infant-Facial-Landmark-Detection-and-Tracking/raw/master/data/300w/300w_valid.csv)

# Stakeholder feedback (03/28/2023)

- feedback regarding scaling methods

The end goal of choosing a better scaling method should be more clear.

- feedback regarding outlier detection

We should know what an outlier looks like, e.g. landmark dots cannot make up a face. And how they can be detected.

Current generic algorithms for detecting outliers may not correctly mean there is no outlier. The applied metrics may not detect the bias, or the metrics may not correspond to the outlier that we tended to look for.

The current landmark results should be reasonable as they have checked them. However, We can put in an outlier on purpose to test whether the detector can detect the outlier.

Instead of using euclidean distances as outlier detection features, try only using normalized coordinates (68-dimensional vector).

Apply PCA to coordinates, and see what the left face shape and the left data look like. Then think about whether the data after PCA is outliers.

- other feedback

Don't focus too much on implementing classification algorithms but on understanding the nature of data.


# EDA

Our exploratory data analysis (EDA) will focus on understanding the distribution of the landmark data and identifying any patterns or relationships that may exist within the data. To accomplish this, we will use a combination of below methodologies:

- Preprocess

1. Scale the data using three different methods: Min-Max Scaling, Z-Score Scaling, and Unit Vector Scaling. Compare them and choose one method to use as the final scale methods.
2. Calculate the Euclidean distance between each pair of variables.
3. Calculate the mean, median, standard deviation, and range for each method and the initial data, and plot boxplot for each variable in the data to gain insights into the distribution and identify potential outliers, and check them using Mahalanobis distance. Compare the results and determine which outliers should be removed.

- Analyze the insights of landmarks

1. Consider which distances to plot by grouping them into relevant categories, such as bounding box size, interocular distance, and length of the shortest/longest dimension.
2. Plot the distances using histograms and Gaussian distributions, grouping them into relevant categories. Consider which distances reveal meaningful differences between variables.
3. Analyze the selection of the center point and rotation axis during the normalization process of landmark data. Are the methods used by the previous project team optimal? Is there a difference in the final facial expression recognition effect? Use data models to verify.
4. Plot regression analyses on the distances to identify patterns and relationships between them. (?) Investigate the geometric relationship between landmark coordinates. Analyze the characteristics of correct facial landmark models - whether a standard pattern can be established, or whether incorrect landmarks can be eliminated in advance.
5. Analyze the data according to face attributes(turned, tilted, occluded, and expressive). Identify differences in landmark points between attributes to gain further insights into the data.

Our EDA will provide valuable insights into the landmark data and help guide the preprocessing and analysis phases of the project. We plan to document our findings in a Markdown file and include detailed explanations of our thought process and any conclusions we draw from the data. We also plan to include code snippets and visualizations that
demonstrate our methods and results.

# Timeline

- Week 1, 03/13 - 03/19: Data preprocessing, scaling method identification and euclidean distances calculation.
- Week 2, 03/20 - 03/26: Outlier removal and geometric relationship investigation
- Week 3, 03/27 - 04/02: Regression and distribution analyses
- Week 4, 04/03 - 04/09: Analysis of landmark data and face attributes
- Week 5, 04/10 - 04/16: Final report and presentation preparation.
- Week 6, 04/17 - 04/23: Presentation and final submission.

# Roles & responsibilities

- Yun Cao: Team Leader. Responsible for project advancement, progress confirmation, task splitting, etc. Next, will be responsible for building the project and scaling the raw data.
- Liyang Song: Team Member. Participating in project discussions, making suggestions, obtaining raw data, etc. Next, will be responsible for processing and analyzing Euclidean distances.
- Na Yin: Team Member. Participating in project discussions and making suggestions. Next, will be responsible for the determination and analysis of outliers.
- All team members will contribute to the final report and presentation
- A front-facing HTML page or markdown file will be created by the team to present results concisely to the stakeholder.

# Issues

- How to determine the optimal scaling method for the landmark data and evaluate its effectiveness.

- Which Euclidean distances and related calculations would be useful in the analysis and identification of patterns and relationships between landmark points, and how to verify their accuracy and availability.

- How to evaluate the effectiveness of the selection of the rotation axis during the normalization process of landmark data.

  