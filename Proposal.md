# Preprocessing of Image Landmarks and Analysis of Relationship with Attributes

**Overview:**

The proposed program is based on the paper "InfAnFace: Bridging the Infant–Adult Domain Gap" by Yang et al. (2021), and a private program "DS5110/faces" coming from DS5110 on the 2022 Fall semester. The program aims to analyze the initial landmark data, detect the variable relations of common landmarks, preprocess the landmark data to a normalized format, and analyze the relationship between the initial landmark data and face attributes including turned, tilted, occluded, and expressive. The program will use statistical learning algorithms and techniques to detect, preprocess, and analyze the landmark data. The program aims to analyze the commonalities and differences of landmark data in image, with helping improve the accuracy and efficiency on potential applications in face recognition and expression recognition.

**Objectives:**

- Analyze the pattern and distribution of the initial landmark data, detect the outliers of them, and find the core and principles on normalizing the landmark data.
- Develop an image processing pipeline that preprocesses landmark data and prepares it for analysis.
- Analyze the relationship between landmark data and face attributes including turned, tilted, occluded, and expressive.

**Methodology:**

The proposed program will be divided into the following phases:

1. Scale the data using three different methods: Min-Max Scaling, Z-Score Scaling, and Unit Vector Scaling.
2. Calculate the mean, median, standard deviation, and range for each method and the initial data, and plot boxplots for each variable in the data to gain insights into the distribution and identify potential outliers, and choose one method to use as the final scale methods.
3. Identify potential outliers using the boxplots, then check them using Mahalanobis distance. Compare the results and determine which outliers should be removed.
4. Calculate the Euclidean distance between each pair of variables. Plot the distances using histograms and Gaussian distributions, grouping them into relevant categories. Consider which distances reveal meaningful differences between variables.
5. Consider which distances to plot by grouping them into relevant categories, such as bounding box size, interocular distance, and length of the shortest/longest dimension.
6. Analyze the selection of the center point and rotation axis during the normalization process of landmark data. Are the methods used by the previous project team optimal? Is there a difference in the final facial expression recognition effect? Use data models to verify.
7. Plot regression analyses on the distances to identify patterns and relationships between them. (?) Investigate the geometric relationship between landmark coordinates. Analyze the characteristics of correct facial landmark models - whether a standard pattern can be established, or whether incorrect landmarks can be eliminated in advance.
8.  Analyze the data according to face attributes(turned, tilted, occluded, and expressive). Identify differences in landmark points between attributes to gain further insights into the data.

**Expected Outcomes:**

The proposed program is expected to achieve the following outcomes:

- A recommended scaling method for the landmark data.
- An identified set of outliers to remove from the data.
- Regression and distribution analyses of Euclidean distances between landmark points, which may provide useful insights.
- A rotation method including choosing the center point and rotation axis.
- Identification of landmark differences between different types of faces (turned, tilted, occluded, and expressive), which could aid in developing a computer algorithm for identifying these types of faces.

**Roles & Responsibilities:**
- Yun Cao: Team Leader. Responsible for project advancement, progress confirmation, task splitting, etc. Next, will be responsible for building the project and scaling the raw data.
- Liyang Song: Team Member. Participating in project discussions, making suggestions, obtaining raw data, etc. Next, will be responsible for processing and analyzing Euclidean distances.
- Na Yin: Team Member. Participating in project discussions and making suggestions. Next, will be responsible for the determination and analysis of outliers

**Background:**

The proposed program is based on the paper "InfAnFace: Bridging the Infant–Adult Domain Gap" by Yang et al. (2021), which proposes a deep neural network model that can bridge the domain gap between infant and adult face recognition. The model uses facial landmarks as input features and achieves state-of-the-art performance on the infant and adult face recognition tasks. The proposed program builds on this work by developing an image processing pipeline that preprocesses landmark data and analyzes the relationship between the landmark data and attributes such as turned, tilted, occluded, and expressive.

**References:**

Yang, Z., Li, Q., Li, J., Chen, C., & Liu, J. (2021). InfAnFace: Bridging the Infant–Adult Domain Gap. IEEE Transactions on Pattern Analysis and Machine Intelligence, 43(3), 951-964.

Jesse Hautala, Sophia Cofone, Zongyu Wu, Connor Lynch, DS5110/faces[Source code]. https://github.com/ds5110/faces

