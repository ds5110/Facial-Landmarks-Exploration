# Introduction

The project focused on the computer vision project in DS5110.

### Reproduce Instruction

- `make data`: The command is used for get initial landmark data.
- `make scale`: The command is used for scale initial data into a normalized format.
- `make scale_analyze`: The command is used for computing the Procrustes Distance of different scale ways.
- `make scale_plt`: The command is used for generating a vision inspection of scale results.

### Feasibility

- Story: Preprocessing of Image Landmarks and Analysis of Relationship with Attributes
- Data: [InfAnFace dataset](https://coe.northeastern.edu/Research/AClab/InfAnFace/)
  , [300-W](https://ibug.doc.ic.ac.uk/resources/300-W/)
- EDA:
    - A recommended scaling method for the landmark data.
    - An identified set of outliers to remove from the data.
    - Regression and distribution analyses of Euclidean distances between landmark points, which may provide useful
      insights.
    - A rotation method including choosing the center point and rotation axis.
    - Identification of landmark differences between different types of faces (turned, tilted, occluded, and expressive)
      , which could aid in developing a computer algorithm for identifying these types of faces.

### Information from Professor

Stakeholder: Michael Wan, PhD, Senior Computational Scientist in Northeastern’s Augmented Cognition Lab

Story/Goal: This computer-vision project will build on and complement a DS 5110 project from fall 2022 that used simple
ML models to distinguish adult & infant faces in images. The project will involve traditional machine learning
teachniques (i.e., no deep learning).

Data: Dr. Wan has been working with facial landmark coordinates from 300-W (adults) and InfAnFace (infants) datasets as
described in InfAnFace paper, Wan et al, (2022) (2022) – arxiv.org

# Team members(Alphabetical Order)

Liyang Song, Na Yin, Yun Cao
