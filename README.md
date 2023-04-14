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
estimation, and facial recognition systems. Our main result is put on the [overview.md](./docs/overview.md), and the
technical details are written in the [techDocs.md](./techDocs.md)

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
- `make feature`: The command is used for feature selection method implementation. This step can be very time-consuming up to tens of minutes. Results are saved as CSV files.
- `make feature_plots`: The command is used for generating feature selection related figures.
- `make feature_scale`: Feature selection implementation with data source changed to `rotated_scale.csv` for comparison.
- `make feature_plots_scale`: Feature selection figures with data source changed to `rotated_scale.csv` for comparison.

## Results

#### Scale

Our in-depth analysis of various scaling and rotation methods can be found in the [scale.md](./docs/scale.md)  file. In
summary, we
discovered that the Multidimensional Scaling (MDS) method altered face orientation, making it unsuitable for our
objectives, while the Standardization method used the mean as the zero point instead of the 33 nose point, which we
decided to ignore. The original
method and Normalization by Bounding Box demonstrated similar results, making it challenging to determine the most
effective approach.

Our work contributes to understanding the impact of different scaling and rotation techniques on facial landmarks, as
presented in the [scale.md](./docs/scale.md)  file. These insights can be valuable for various facial analysis tasks and
future research.

## Attribution

Primary project and data sources:

- [InfAnFace: Bridging the Infant--Adult Domain Gap in Facial Landmark Estimation in the Wild](https://github.com/ostadabbas/Infant-Facial-Landmark-Detection-and-Tracking):
  This foundational project offers the original facial landmarks for both infants and adults, which serve as the core of
  our analysis.

- [DS5110 faces](https://github.com/ds5110/faces): This valuable project supplies a substantial methodology for
  preprocessing facial landmarks and evaluating the distinctions between infant and adult landmarks.

Team members and their contributions:

- Yun Cao: Yun was responsible for completing the scaling component of the program, organizing team meetings, overseeing
  the project's timeline and progress, and offering guidance and advices to issues encountered.
- Na Yin: Na completed the outlier segment of the program, participated in team meetings, adhered to deadlines, and
  contributed to discussions, providing advice to address project-related concerns.
- Liyang Song: Liyang exhibited exceptional proficiency in completing the feature selection portion of the program. He
  consistently attended team meetings and diligently completed assigned tasks on time. Liyang's innovative and
  perceptive approach to data analysis significantly contributed to the project's success. His keen insights and
  creative problem-solving skills were invaluable assets to the team.

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