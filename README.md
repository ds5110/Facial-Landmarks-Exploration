## Introduction

The project focused on the Computer Vision project in course DS5110 in Spring 2023 semester, mainly on enhancing facial
landmark alignment, representation, and feature selection techniques in the context of computer vision and facial
recognition. Based on the [InfAnFace paper, Wan et al, (2022)](https://arxiv.org/abs/2110.08935) and
the [faces project](https://github.com/ds5110/faces), our work is divided into three main components: exploring various
scaling and rotation methods, outlier detection, and feature selection.

1. **Scaling and Rotation**: We compare the original method with three alternatives: Multidimensional Scaling (MDS),
   Standardization, and Normalization by Bounding Box. Our goal is to evaluate the impact of these methods on facial
   landmark alignment and representation.
2. **Outlier Detection**: We implement outlier detection using the Mahalanobis distance and Isolation Forest algorithms.
   This step aims to identify and remove any anomalous data points that might negatively impact the accuracy of the
   facial analysis.
3. **Feature Selection**: We explore feature selection techniques, using Recursive Feature Elimination (RFE) and the
   forward selection algorithm, to identify the most relevant features for our facial recognition tasks.

By assessing the effectiveness of different techniques in these three areas, we aim to contribute to the development of
more accurate and robust facial analysis algorithms. Our work has potential applications in emotion detection, age
estimation, and facial recognition systems.

## Environment

```shell
conda env create -f environment.yml
```

## Reproduce Instruction

Execute below command before executing other commands:

```shell
conda activate DS5110-faces-extend
```

- `make scale`: The command is used for downloading data and calculating the scale part.
- `make euclidean`: The command is used for generating euclidean distances between landmarks.
- `make if_outlier_infant`: The command is used for selecting outliers in infant dataset using Isolation Forest .
- `make if_outlier_adult`: The command is used for selecting outliers in adult dataset using Isolation Forest.
- `make ma_outlier_infant`: The command is used for selecting outliers in infant dataset using Mahalanobis distance .
- `make ma_outlier_adult`: The command is used for selecting outliers in adult dataset using Mahalanobis distance.
- `make pic`: The command is used for showing the picture with landmarks.

## Results

#### Scale

Our in-depth analysis of various scaling and rotation methods can be found in the [scale.md](./scale.md)  file. In
summary, we
discovered that the Multidimensional Scaling (MDS) method altered face orientation, making it unsuitable for our
objectives, while the Standardization method used the mean as the zero point instead of the 33 nose point, which we
decided to ignore. The original
method and Normalization by Bounding Box demonstrated similar results, making it challenging to determine the most
effective approach.

Our work contributes to understanding the impact of different scaling and rotation techniques on facial landmarks, as
presented in the [scale.md](./scale.md)  file. These insights can be valuable for various facial analysis tasks and
future research.

## Contributors

Team members: Liyang Song, Na Yin, Yun Cao

## Acknowledgments

We would like to express our gratitude to our
professor, [Philip Bodgen](https://www.khoury.northeastern.edu/people/philip-bogden/), for his guidance, support, and
encouragement
throughout the course of this project, and to our
Stakeholder, [Michael Wan](https://roux.northeastern.edu/people/michael-wan/), Ph.D., Senior Computational Scientist in
Northeastern's Augmented Cognition Lab, for his valuable guidance and support. We also want to extend our appreciation
to [ChatGPT](https://chat.openai.com/), an AI language model, for its assistance in various stages of the project,
including research, analysis, and
documentation.

Our appreciation goes to the study of the [InfAnFace paper, Wan et al, (2022)](https://arxiv.org/abs/2110.08935),
co-authored by Michael Wan and his
colleagues, which provided us with the opportunity to delve deeper into the analysis of infant landmarks. Lastly, we
want to thank the [DS 5110 project from fall 2022](https://github.com/ds5110/faces), developed by a group of students
during the 2022 Fall semester, for
allowing us to focus on the details of the task and build upon their initial efforts.