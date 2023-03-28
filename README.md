# Introduction

The project focused on the Computer Vision project in course DS5110 in Spring 2023 semester.

### Reproduce Instruction

- `make data`: The command is used for getting initial landmark data.
- `make scale`: The command is used for scaling initial data into a normalized format.
- `make scale_plt`: The command is used for generating a visual inspection of scale results.
- `make euclidean`: The command is used for generating euclidean distances between landmarks.
- `make if_outlier_infant`: The command is used for selecting outliers in infant dataset using Isolation Forest .
- `make if_outlier_adult`: The command is used for selecting outliers in adult dataset using Isolation Forest.
- `make ma_outlier_infant`: The command is used for selecting outliers in infant dataset using Mahalanobis distance .
- `make ma_outlier_adult`: The command is used for selecting outliers in adult dataset using Mahalanobis distance.
- `make pic`: The command is used for showing the picture with landmarks.
  

### Feasibility

- Story: Preprocessing of Image Landmarks and Analysis of Relationship with Attributes.

- Data: [InfAnFace dataset](https://coe.northeastern.edu/Research/AClab/InfAnFace/)
  , [300-W](https://ibug.doc.ic.ac.uk/resources/300-W/)

- EDA:
    - A recommended [scaling method](./scale.md) for the landmark data.
    - An identified set of outliers to remove from the data.
    - Regression and distribution analyses of Euclidean distances between landmark points, which may provide useful
      insights.
    - A rotation method including choosing the center point and rotation axis.
    - Identification of landmark differences between different types of faces (turned, tilted, occluded, and expressive)
      , which could aid in developing a computer algorithm for identifying these types of faces.

### Information from Professor

Stakeholder: Michael Wan, Ph.D, Senior Computational Scientist in Northeastern’s Augmented Cognition Lab.

Story/Goal: This computer-vision project will build on and complement
a [DS 5110 project from fall 2022](https://github.com/ds5110/faces) that used simple ML models to distinguish adult &
infant faces in images. The project will involve traditional machine learning techniques (i.e., no deep learning).

Data: Dr. Wan has been working with facial landmark coordinates from 300-W (adults) and InfAnFace (infants) datasets as
described in [InfAnFace paper, Wan et al, (2022)](https://arxiv.org/abs/2110.08935) (2022) – arxiv.org.

# Team members(Alphabetical Order)

Liyang Song, Na Yin, Yun Cao
