# Investigating the Best Way to Select Outliers

## Introduction

Outliers are exceptional records that are significantly different from the rest of the data. Commonly, they can lead to incorrect conclusions or predictions and will have an impact on further research. Therefore, outliers selection is an important part of data analysis and a step we must go through before using model to train or test. Considering the multidimensional data, Mahalanobis distance and Isolation Forest are two commonly used techniques for identifying outliers in landmarks data. In this approach, we utilize these two techniques to detect outliers and validate the model's accuracy using noise data.  

## Data Analysis  

### Mean, median, standard deviation, and range for each variable
To gain insights into the distribution of our data, we performed a data analysis by calculating the mean, median, standard deviation, and range for each variable. 

The data source is `merged_landmarks`. The shapes of the infant dataset and adult dataset are (410, 136) (689, 136) respectively.

```agsl
python src/scatter.py
Column x0: Mean=-0.47, Median=-0.48, Std=0.21, Range=1.06
Column y0: Mean=-0.25, Median=-0.27, Std=0.19, Range=1.29
Column x1: Mean=-0.46, Median=-0.48, Std=0.20, Range=1.06
Column y1: Mean=-0.11, Median=-0.12, Std=0.18, Range=1.20
Column x2: Mean=-0.45, Median=-0.46, Std=0.18, Range=1.01
Column y2: Mean=0.02, Median=0.01, Std=0.18, Range=1.11
Column x3: Mean=-0.42, Median=-0.43, Std=0.16, Range=0.97
Column y3: Mean=0.14, Median=0.14, Std=0.17, Range=1.13
Column x4: Mean=-0.37, Median=-0.39, Std=0.14, Range=0.86
Column y4: Mean=0.25, Median=0.25, Std=0.15, Range=0.99
Column x5: Mean=-0.31, Median=-0.32, Std=0.12, Range=0.75
Column y5: Mean=0.34, Median=0.34, Std=0.13, Range=0.85
Column x6: Mean=-0.23, Median=-0.24, Std=0.10, Range=0.74
Column y6: Mean=0.40, Median=0.40, Std=0.10, Range=0.70
Column x7: Mean=-0.14, Median=-0.15, Std=0.09, Range=0.73
Column y7: Mean=0.45, Median=0.46, Std=0.08, Range=0.60
Column x8: Mean=-0.00, Median=0.00, Std=0.08, Range=0.68
Column y8: Mean=0.51, Median=0.51, Std=0.08, Range=0.60
Column x9: Mean=0.14, Median=0.15, Std=0.09, Range=0.83
Column y9: Mean=0.46, Median=0.46, Std=0.08, Range=0.57
Column x10: Mean=0.24, Median=0.25, Std=0.11, Range=0.98
Column y10: Mean=0.41, Median=0.41, Std=0.10, Range=0.62
Column x11: Mean=0.32, Median=0.33, Std=0.13, Range=1.01
Column y11: Mean=0.35, Median=0.35, Std=0.12, Range=0.76
Column x12: Mean=0.40, Median=0.41, Std=0.14, Range=0.96
Column y12: Mean=0.27, Median=0.26, Std=0.14, Range=0.95
Column x13: Mean=0.45, Median=0.46, Std=0.16, Range=0.93
Column y13: Mean=0.16, Median=0.15, Std=0.17, Range=1.09
Column x14: Mean=0.48, Median=0.48, Std=0.18, Range=1.00
Column y14: Mean=0.04, Median=0.03, Std=0.19, Range=1.15
Column x15: Mean=0.49, Median=0.51, Std=0.20, Range=1.04
Column y15: Mean=-0.08, Median=-0.10, Std=0.19, Range=1.18
Column x16: Mean=0.50, Median=0.51, Std=0.21, Range=1.04
Column y16: Mean=-0.22, Median=-0.25, Std=0.20, Range=1.25
Column x17: Mean=-0.35, Median=-0.38, Std=0.13, Range=0.64
Column y17: Mean=-0.39, Median=-0.40, Std=0.09, Range=0.49
Column x18: Mean=-0.29, Median=-0.32, Std=0.11, Range=0.59
Column y18: Mean=-0.44, Median=-0.44, Std=0.08, Range=0.46
Column x19: Mean=-0.23, Median=-0.25, Std=0.10, Range=0.54
Column y19: Mean=-0.46, Median=-0.47, Std=0.07, Range=0.44
Column x20: Mean=-0.17, Median=-0.18, Std=0.09, Range=0.49
Column y20: Mean=-0.45, Median=-0.46, Std=0.07, Range=0.40
Column x21: Mean=-0.11, Median=-0.12, Std=0.08, Range=0.46
Column y21: Mean=-0.43, Median=-0.44, Std=0.07, Range=0.38
Column x22: Mean=0.13, Median=0.14, Std=0.07, Range=0.44
Column y22: Mean=-0.43, Median=-0.44, Std=0.07, Range=0.38
Column x23: Mean=0.19, Median=0.20, Std=0.08, Range=0.47
Column y23: Mean=-0.45, Median=-0.46, Std=0.07, Range=0.39
Column x24: Mean=0.25, Median=0.27, Std=0.09, Range=0.53
Column y24: Mean=-0.45, Median=-0.46, Std=0.07, Range=0.41
Column x25: Mean=0.31, Median=0.33, Std=0.10, Range=0.61
Column y25: Mean=-0.44, Median=-0.45, Std=0.08, Range=0.45
Column x26: Mean=0.36, Median=0.38, Std=0.12, Range=0.68
Column y26: Mean=-0.40, Median=-0.41, Std=0.09, Range=0.51
Column x27: Mean=0.01, Median=0.00, Std=0.04, Range=0.32
Column y27: Mean=-0.29, Median=-0.30, Std=0.05, Range=0.30
Column x28: Mean=0.00, Median=0.00, Std=0.03, Range=0.24
Column y28: Mean=-0.22, Median=-0.23, Std=0.03, Range=0.23
Column x29: Mean=0.00, Median=0.00, Std=0.02, Range=0.16
Column y29: Mean=-0.16, Median=-0.16, Std=0.03, Range=0.19
Column x30: Mean=0.00, Median=0.00, Std=0.03, Range=0.18
Column y30: Mean=-0.10, Median=-0.10, Std=0.03, Range=0.23
Column x31: Mean=-0.09, Median=-0.08, Std=0.03, Range=0.16
Column y31: Mean=-0.00, Median=-0.01, Std=0.02, Range=0.10
Column x32: Mean=-0.04, Median=-0.04, Std=0.01, Range=0.09
Column y32: Mean=-0.00, Median=-0.00, Std=0.01, Range=0.09
Column x33: Mean=0.00, Median=0.00, Std=0.00, Range=0.00
Column y33: Mean=0.00, Median=0.00, Std=0.00, Range=0.00
Column x34: Mean=0.05, Median=0.05, Std=0.01, Range=0.09
Column y34: Mean=-0.00, Median=-0.00, Std=0.01, Range=0.08
Column x35: Mean=0.09, Median=0.09, Std=0.03, Range=0.18
Column y35: Mean=-0.00, Median=-0.00, Std=0.02, Range=0.11
Column x36: Mean=-0.29, Median=-0.31, Std=0.10, Range=0.57
Column y36: Mean=-0.26, Median=-0.26, Std=0.08, Range=0.46
Column x37: Mean=-0.23, Median=-0.25, Std=0.08, Range=0.49
Column y37: Mean=-0.30, Median=-0.31, Std=0.08, Range=0.43
Column x38: Mean=-0.17, Median=-0.19, Std=0.07, Range=0.41
Column y38: Mean=-0.31, Median=-0.31, Std=0.07, Range=0.40
Column x39: Mean=-0.11, Median=-0.13, Std=0.07, Range=0.40
Column y39: Mean=-0.27, Median=-0.27, Std=0.06, Range=0.37
Column x40: Mean=-0.17, Median=-0.18, Std=0.07, Range=0.41
Column y40: Mean=-0.24, Median=-0.24, Std=0.06, Range=0.34
Column x41: Mean=-0.23, Median=-0.25, Std=0.08, Range=0.46
Column y41: Mean=-0.24, Median=-0.24, Std=0.06, Range=0.36
Column x42: Mean=0.13, Median=0.14, Std=0.07, Range=0.42
Column y42: Mean=-0.26, Median=-0.26, Std=0.06, Range=0.36
Column x43: Mean=0.18, Median=0.19, Std=0.07, Range=0.44
Column y43: Mean=-0.30, Median=-0.31, Std=0.07, Range=0.41
Column x44: Mean=0.24, Median=0.26, Std=0.08, Range=0.50
Column y44: Mean=-0.30, Median=-0.30, Std=0.08, Range=0.45
Column x45: Mean=0.30, Median=0.32, Std=0.10, Range=0.58
Column y45: Mean=-0.26, Median=-0.27, Std=0.08, Range=0.46
Column x46: Mean=0.25, Median=0.27, Std=0.08, Range=0.49
Column y46: Mean=-0.24, Median=-0.24, Std=0.06, Range=0.39
Column x47: Mean=0.19, Median=0.20, Std=0.07, Range=0.43
Column y47: Mean=-0.24, Median=-0.24, Std=0.06, Range=0.37
Column x48: Mean=-0.15, Median=-0.16, Std=0.06, Range=0.46
Column y48: Mean=0.21, Median=0.21, Std=0.05, Range=0.31
Column x49: Mean=-0.10, Median=-0.10, Std=0.04, Range=0.31
Column y49: Mean=0.15, Median=0.15, Std=0.03, Range=0.22
Column x50: Mean=-0.04, Median=-0.04, Std=0.03, Range=0.23
Column y50: Mean=0.11, Median=0.11, Std=0.03, Range=0.20
Column x51: Mean=-0.00, Median=0.00, Std=0.03, Range=0.23
Column y51: Mean=0.12, Median=0.12, Std=0.03, Range=0.19
Column x52: Mean=0.03, Median=0.04, Std=0.03, Range=0.26
Column y52: Mean=0.11, Median=0.11, Std=0.03, Range=0.19
Column x53: Mean=0.10, Median=0.10, Std=0.04, Range=0.37
Column y53: Mean=0.15, Median=0.15, Std=0.03, Range=0.17
Column x54: Mean=0.16, Median=0.16, Std=0.07, Range=0.63
Column y54: Mean=0.21, Median=0.21, Std=0.05, Range=0.36
Column x55: Mean=0.10, Median=0.11, Std=0.06, Range=0.58
Column y55: Mean=0.27, Median=0.26, Std=0.06, Range=0.35
Column x56: Mean=0.05, Median=0.06, Std=0.05, Range=0.50
Column y56: Mean=0.29, Median=0.29, Std=0.06, Range=0.38
Column x57: Mean=0.00, Median=0.00, Std=0.04, Range=0.43
Column y57: Mean=0.30, Median=0.29, Std=0.07, Range=0.40
Column x58: Mean=-0.05, Median=-0.05, Std=0.04, Range=0.41
Column y58: Mean=0.29, Median=0.29, Std=0.06, Range=0.40
Column x59: Mean=-0.10, Median=-0.10, Std=0.05, Range=0.45
Column y59: Mean=0.27, Median=0.26, Std=0.06, Range=0.39
Column x60: Mean=-0.13, Median=-0.14, Std=0.06, Range=0.43
Column y60: Mean=0.21, Median=0.21, Std=0.05, Range=0.33
Column x61: Mean=-0.05, Median=-0.05, Std=0.04, Range=0.35
Column y61: Mean=0.17, Median=0.16, Std=0.03, Range=0.21
Column x62: Mean=-0.00, Median=-0.00, Std=0.03, Range=0.29
Column y62: Mean=0.16, Median=0.16, Std=0.03, Range=0.20
Column x63: Mean=0.04, Median=0.05, Std=0.04, Range=0.39
Column y63: Mean=0.17, Median=0.17, Std=0.03, Range=0.18
Column x64: Mean=0.13, Median=0.13, Std=0.06, Range=0.58
Column y64: Mean=0.21, Median=0.21, Std=0.04, Range=0.29
Column x65: Mean=0.05, Median=0.05, Std=0.05, Range=0.52
Column y65: Mean=0.23, Median=0.23, Std=0.06, Range=0.35
Column x66: Mean=0.00, Median=0.00, Std=0.04, Range=0.44
Column y66: Mean=0.24, Median=0.23, Std=0.07, Range=0.38
Column x67: Mean=-0.05, Median=-0.04, Std=0.05, Range=0.43
Column y67: Mean=0.23, Median=0.23, Std=0.06, Range=0.34
Column x0: Mean=-0.49, Median=-0.50, Std=0.17, Range=0.81
Column y0: Mean=-0.34, Median=-0.34, Std=0.12, Range=0.97
Column x1: Mean=-0.48, Median=-0.49, Std=0.17, Range=0.78
Column y1: Mean=-0.21, Median=-0.21, Std=0.11, Range=0.93
Column x2: Mean=-0.47, Median=-0.47, Std=0.16, Range=0.76
Column y2: Mean=-0.07, Median=-0.08, Std=0.11, Range=0.90
Column x3: Mean=-0.44, Median=-0.45, Std=0.16, Range=0.72
Column y3: Mean=0.06, Median=0.05, Std=0.10, Range=0.87
Column x4: Mean=-0.39, Median=-0.41, Std=0.14, Range=0.68
Column y4: Mean=0.18, Median=0.18, Std=0.10, Range=0.80
Column x5: Mean=-0.31, Median=-0.33, Std=0.12, Range=0.61
Column y5: Mean=0.29, Median=0.29, Std=0.09, Range=0.65
Column x6: Mean=-0.22, Median=-0.23, Std=0.10, Range=0.54
Column y6: Mean=0.38, Median=0.38, Std=0.07, Range=0.55
Column x7: Mean=-0.12, Median=-0.12, Std=0.07, Range=0.54
Column y7: Mean=0.46, Median=0.46, Std=0.06, Range=0.47
Column x8: Mean=0.01, Median=0.00, Std=0.07, Range=0.57
Column y8: Mean=0.48, Median=0.48, Std=0.05, Range=0.43
Column x9: Mean=0.12, Median=0.12, Std=0.07, Range=0.58
Column y9: Mean=0.45, Median=0.45, Std=0.06, Range=0.44
Column x10: Mean=0.23, Median=0.23, Std=0.09, Range=0.63
Column y10: Mean=0.38, Median=0.38, Std=0.07, Range=0.52
Column x11: Mean=0.32, Median=0.33, Std=0.12, Range=0.69
Column y11: Mean=0.29, Median=0.29, Std=0.09, Range=0.66
Column x12: Mean=0.40, Median=0.41, Std=0.14, Range=0.71
Column y12: Mean=0.18, Median=0.18, Std=0.10, Range=0.70
Column x13: Mean=0.45, Median=0.45, Std=0.15, Range=0.74
Column y13: Mean=0.06, Median=0.05, Std=0.10, Range=0.75
Column x14: Mean=0.48, Median=0.48, Std=0.16, Range=0.73
Column y14: Mean=-0.07, Median=-0.08, Std=0.11, Range=0.81
Column x15: Mean=0.49, Median=0.49, Std=0.16, Range=0.75
Column y15: Mean=-0.21, Median=-0.21, Std=0.11, Range=0.88
Column x16: Mean=0.50, Median=0.50, Std=0.17, Range=0.84
Column y16: Mean=-0.34, Median=-0.34, Std=0.12, Range=0.95
Column x17: Mean=-0.39, Median=-0.41, Std=0.10, Range=0.72
Column y17: Mean=-0.44, Median=-0.44, Std=0.07, Range=0.49
Column x18: Mean=-0.33, Median=-0.35, Std=0.08, Range=0.67
Column y18: Mean=-0.49, Median=-0.49, Std=0.06, Range=0.43
Column x19: Mean=-0.25, Median=-0.26, Std=0.07, Range=0.58
Column y19: Mean=-0.50, Median=-0.51, Std=0.05, Range=0.34
Column x20: Mean=-0.17, Median=-0.17, Std=0.05, Range=0.47
Column y20: Mean=-0.49, Median=-0.49, Std=0.04, Range=0.31
Column x21: Mean=-0.09, Median=-0.09, Std=0.05, Range=0.38
Column y21: Mean=-0.46, Median=-0.46, Std=0.04, Range=0.30
Column x22: Mean=0.08, Median=0.09, Std=0.04, Range=0.40
Column y22: Mean=-0.46, Median=-0.47, Std=0.04, Range=0.31
Column x23: Mean=0.17, Median=0.17, Std=0.05, Range=0.43
Column y23: Mean=-0.49, Median=-0.50, Std=0.04, Range=0.30
Column x24: Mean=0.25, Median=0.26, Std=0.06, Range=0.48
Column y24: Mean=-0.51, Median=-0.51, Std=0.05, Range=0.38
Column x25: Mean=0.33, Median=0.35, Std=0.07, Range=0.61
Column y25: Mean=-0.49, Median=-0.49, Std=0.06, Range=0.49
Column x26: Mean=0.39, Median=0.41, Std=0.09, Range=0.77
Column y26: Mean=-0.44, Median=-0.44, Std=0.07, Range=0.51
Column x27: Mean=-0.00, Median=0.00, Std=0.03, Range=0.29
Column y27: Mean=-0.35, Median=-0.36, Std=0.04, Range=0.23
Column x28: Mean=-0.00, Median=0.00, Std=0.02, Range=0.20
Column y28: Mean=-0.27, Median=-0.27, Std=0.02, Range=0.14
Column x29: Mean=-0.00, Median=0.00, Std=0.02, Range=0.17
Column y29: Mean=-0.18, Median=-0.18, Std=0.02, Range=0.11
Column x30: Mean=-0.00, Median=0.00, Std=0.03, Range=0.22
Column y30: Mean=-0.09, Median=-0.09, Std=0.03, Range=0.17
Column x31: Mean=-0.10, Median=-0.10, Std=0.02, Range=0.13
Column y31: Mean=-0.03, Median=-0.03, Std=0.02, Range=0.15
Column x32: Mean=-0.05, Median=-0.05, Std=0.01, Range=0.07
Column y32: Mean=-0.02, Median=-0.01, Std=0.01, Range=0.07
Column x33: Mean=0.00, Median=0.00, Std=0.00, Range=0.00
Column y33: Mean=0.00, Median=0.00, Std=0.00, Range=0.00
Column x34: Mean=0.05, Median=0.05, Std=0.01, Range=0.08
Column y34: Mean=-0.02, Median=-0.02, Std=0.01, Range=0.07
Column x35: Mean=0.09, Median=0.09, Std=0.02, Range=0.15
Column y35: Mean=-0.03, Median=-0.03, Std=0.02, Range=0.15
Column x36: Mean=-0.30, Median=-0.31, Std=0.08, Range=0.46
Column y36: Mean=-0.34, Median=-0.34, Std=0.06, Range=0.38
Column x37: Mean=-0.24, Median=-0.25, Std=0.07, Range=0.43
Column y37: Mean=-0.37, Median=-0.38, Std=0.05, Range=0.33
Column x38: Mean=-0.18, Median=-0.19, Std=0.06, Range=0.38
Column y38: Mean=-0.37, Median=-0.37, Std=0.05, Range=0.32
Column x39: Mean=-0.13, Median=-0.13, Std=0.06, Range=0.34
Column y39: Mean=-0.33, Median=-0.33, Std=0.05, Range=0.30
Column x40: Mean=-0.18, Median=-0.19, Std=0.06, Range=0.36
Column y40: Mean=-0.32, Median=-0.32, Std=0.05, Range=0.37
Column x41: Mean=-0.25, Median=-0.26, Std=0.07, Range=0.41
Column y41: Mean=-0.32, Median=-0.32, Std=0.05, Range=0.39
Column x42: Mean=0.12, Median=0.13, Std=0.06, Range=0.45
Column y42: Mean=-0.33, Median=-0.33, Std=0.05, Range=0.31
Column x43: Mean=0.18, Median=0.19, Std=0.06, Range=0.48
Column y43: Mean=-0.37, Median=-0.38, Std=0.05, Range=0.33
Column x44: Mean=0.24, Median=0.25, Std=0.06, Range=0.57
Column y44: Mean=-0.37, Median=-0.38, Std=0.05, Range=0.35
Column x45: Mean=0.30, Median=0.31, Std=0.07, Range=0.62
Column y45: Mean=-0.34, Median=-0.35, Std=0.06, Range=0.37
Column x46: Mean=0.25, Median=0.26, Std=0.06, Range=0.56
Column y46: Mean=-0.32, Median=-0.32, Std=0.05, Range=0.40
Column x47: Mean=0.18, Median=0.19, Std=0.06, Range=0.49
Column y47: Mean=-0.32, Median=-0.32, Std=0.05, Range=0.39
Column x48: Mean=-0.19, Median=-0.19, Std=0.07, Range=0.41
Column y48: Mean=0.13, Median=0.13, Std=0.05, Range=0.33
Column x49: Mean=-0.12, Median=-0.12, Std=0.04, Range=0.30
Column y49: Mean=0.10, Median=0.10, Std=0.03, Range=0.20
Column x50: Mean=-0.05, Median=-0.05, Std=0.03, Range=0.20
Column y50: Mean=0.08, Median=0.08, Std=0.03, Range=0.17
Column x51: Mean=-0.00, Median=-0.00, Std=0.02, Range=0.17
Column y51: Mean=0.09, Median=0.09, Std=0.03, Range=0.16
Column x52: Mean=0.05, Median=0.05, Std=0.02, Range=0.19
Column y52: Mean=0.08, Median=0.08, Std=0.03, Range=0.16
Column x53: Mean=0.12, Median=0.12, Std=0.04, Range=0.31
Column y53: Mean=0.10, Median=0.10, Std=0.03, Range=0.22
Column x54: Mean=0.19, Median=0.20, Std=0.07, Range=0.42
Column y54: Mean=0.13, Median=0.13, Std=0.05, Range=0.33
Column x55: Mean=0.13, Median=0.13, Std=0.05, Range=0.37
Column y55: Mean=0.20, Median=0.20, Std=0.04, Range=0.39
Column x56: Mean=0.06, Median=0.06, Std=0.03, Range=0.34
Column y56: Mean=0.23, Median=0.23, Std=0.05, Range=0.36
Column x57: Mean=0.00, Median=-0.00, Std=0.03, Range=0.34
Column y57: Mean=0.24, Median=0.24, Std=0.05, Range=0.37
Column x58: Mean=-0.05, Median=-0.05, Std=0.04, Range=0.34
Column y58: Mean=0.23, Median=0.23, Std=0.05, Range=0.39
Column x59: Mean=-0.12, Median=-0.12, Std=0.05, Range=0.35
Column y59: Mean=0.20, Median=0.20, Std=0.04, Range=0.37
Column x60: Mean=-0.16, Median=-0.16, Std=0.07, Range=0.41
Column y60: Mean=0.13, Median=0.13, Std=0.05, Range=0.30
Column x61: Mean=-0.05, Median=-0.05, Std=0.03, Range=0.22
Column y61: Mean=0.12, Median=0.13, Std=0.03, Range=0.20
Column x62: Mean=-0.00, Median=-0.00, Std=0.02, Range=0.19
Column y62: Mean=0.13, Median=0.13, Std=0.03, Range=0.18
Column x63: Mean=0.05, Median=0.05, Std=0.03, Range=0.20
Column y63: Mean=0.12, Median=0.13, Std=0.03, Range=0.19
Column x64: Mean=0.16, Median=0.17, Std=0.06, Range=0.40
Column y64: Mean=0.13, Median=0.13, Std=0.05, Range=0.32
Column x65: Mean=0.05, Median=0.05, Std=0.03, Range=0.27
Column y65: Mean=0.17, Median=0.16, Std=0.04, Range=0.37
Column x66: Mean=-0.00, Median=-0.00, Std=0.03, Range=0.29
Column y66: Mean=0.17, Median=0.17, Std=0.04, Range=0.37
Column x67: Mean=-0.05, Median=-0.05, Std=0.03, Range=0.29
Column y67: Mean=0.17, Median=0.16, Std=0.04, Range=0.38

Process finished with exit code 0
```

### Visualization
Additionally, we created boxplot and scatterplot for each variable to visualize their distribution. Boxplots help visualize the distribution of each variable, while scatterplots show the relationship between individual data points.

#### Facial landmarks distribution of infants (values taken as the mean of each landmark)
<div align="center">

![scatter_infant](../outcome/outlier_selection/scatter_infant.png)

</div>

#### Boxplot of infant_x
<div align="center">

![boxplot_infant_x](../outcome/outlier_selection/boxplot_infant_x.png)
</div>

#### Boxplot of infant_y
<div align="center">

![boxplot_infant_y](../outcome/outlier_selection/boxplot_infant_y.png)
</div>

#### Facial landmarks distribution of adults (values taken as the mean of each landmark)
<div align="center">

![scatter_adult](../outcome/outlier_selection/scatter_adult.png)
</div>

#### Boxplot of adult_x
<div align="center">

![boxplot_adult_x](../outcome/outlier_selection/boxplot_adult_x.png)
</div>

#### Boxplot of adult_y
<div align="center">

![boxplot_adult_y](../outcome/outlier_selection/boxplot_adult_y.png)
</div>

### Using two models to detect outliers
The approach we take for detecting outliers involves the use of Mahalanobis distance, and Isolation Forest.Mahalanobis distance to determine the similarity or dissimilarity between data points by scaling the difference by the inverse of the covariance matrix, and then taking the square root of the result to produces a single value that represents the distance between the two points in the multi-dimensional space. During the process,  we compute the Mahalanobis distance for each data point, which measures the distance between a point and a distribution, taking into account the covariance structure of the dataset.Isolation Forest is an anomaly detection algorithm based on tree structures that can detect anomalous data points in a short time. It achieves this by building decision trees with random splits in the dataset, where each tree is a recursive process of dividing the dataset into subsets. During the process, it partitions the dataset into smaller and smaller subspaces until the anomalous points are isolated.  

The results are as follows.

#### __Mahalanobis distance__

```agsl
Data:
infant_outlier:
Outliers: Int64Index([  3,  10,  13,  22,  32,  35,  38,  41,  68,  80,  81,  89,  98,
             99, 109, 142, 239, 277, 335, 381],
           dtype='int64')
adult_outlier:
Outliers: Int64Index([ 21,  28,  40,  55,  66,  76, 149, 167, 170, 180, 226, 244, 269,
            284, 296, 339, 345, 371, 388, 422, 531, 594, 624, 625, 626, 651,
            657, 665, 667, 677, 681, 682],
           dtype='int64')
```
<div align="center">

|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  1 | 1 |
| Precision |1 | 1|
| Recall| 1 | 1 |
| F1 | 1 | 1|

</div>


#### __Isolation Forest__

```agsl
Data:
infant_outlier:
[  3  10  12  13  68  69  80  81  99 142 183 241 258 268 286 288 299 323
 329 364]
adult_outlier:
[ 15  21  28  40 109 163 167 180 226 248 269 284 296 331 335 339 344 355
 356 371 382 395 422 489 574 624 636 651 657 665 667 681]
```

<div align="center">

|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  1 | 1 |
| Precision |1 | 1|
| Recall| 1 | 1 |
| F1 | 1 | 1|
</div>
    
### Assessing the Feasibility of Applying the Model for Outlier

To determine if the results identified by our model are true outliers, we need an appropriate criterion for validation. However, in the absence of such a criterion, we added some noise points to the dataset to test the feasibility of our model. We examined whether the Mahalanobis distance and Isolation Forest techniques could detect these noise points as outliers. If the model is able to identify the noise points as outliers, it would suggest that our analysis is feasible. Conversely, if the model fails to identify the noise points as outliers, it would indicate that our approach may not be effective for outlier detection. By conducting this validation process, we can ensure that our model is robust and reliable in detecting outliers, even in the presence of noise and other irregularities in the data.

Based on the previous analysis of the landmarks data, we observed that all the x and y coordinates were within the range of [-1,1]. Therefore, we added noise points to the dataset with values also restricted to the same range. The proportion of noise points added was set to 5% of the original dataset, resulting in the addition of 20 noise points to the infant dataset and 34 noise points to the adult dataset. The dimensions of the original and modified datasets are as follows: the infant dataset had a dimension of (410, 136) and after adding the noise points, it became (689, 136). Similarly, the adult dataset had a dimension of (430, 136) and became (723, 136) after the addition of noise points. The noise rows index are 411-430 , 690-723 respectively. By incorporating these noise points into the dataset, we can evaluate the effectiveness of our outlier detection model in the presence of noise and ensure that it is robust and reliable in identifying outliers even in more complex datasets.

In summary, the data distributions are as follows.

<div align="center">

|    | noise index | other index(correct index) |
| ---- | ---- | ---- |
| infant | 410-429 | 0-409 |
| adult | 689-722 | 0-688|

</div>

After using two methods, the results are as follows (copy from terminal).

#### __Mahalanobis distance__

```agsl
Use Mahalanobis:
Test the method with noise:
infant_outlier:
[410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427
 428 429]
adult_outlier:
[689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706
 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722]
```

<div align="center">

|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  1 | 1 |
| Precision |1 | 1|
| Recall| 1 | 1 |
| F1 | 1 | 1|

</div>

#### __Isolation Forest__

```agsl
Use isolation tree:
Test the method with noise:
infant_outlier:
Outliers: Int64Index([410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422,
            423, 424, 425, 426, 427, 428, 429],
           dtype='int64')
adult_outlier:
Outliers: Int64Index([689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701,
            702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714,
            715, 716, 717, 718, 719, 720, 721, 722],
           dtype='int64')
```

<div align="center">

|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  1 | 1 |
| Precision |1 | 1|
| Recall| 1 | 1 |
| F1 | 1 | 1|

</div>

### Others related

In addition to using landmarks data, we also examined the effectiveness of our outlier detection model on datasets obtained through three different scaling methods: standard scaling, normalization, and MDS scaling.

Results are as follows.

#### Standard

```agsl
Use isolation tree:
Test the method with noise:
infant_outlier:
Outliers: Int64Index([410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422,
            423, 424, 425, 426, 427, 428, 429],
           dtype='int64')
adult_outlier:
Outliers: Int64Index([689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701,
            702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714,
            715, 716, 717, 718, 719, 720, 721, 722],
           dtype='int64')
------------------------------------------------------------
Use Mahalanobis:
Test the method with noise:
infant_outlier:
[410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427
 428 429]
adult_outlier:
[689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706
 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722]
```

<div align="center">

|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  1 | 1 |
| Precision |1 | 1|
| Recall| 1 | 1 |
| F1 | 1 | 1|
</div>

#### Normalized

```agsl
Use isolation tree:
Test the method with noise:
infant_outlier:
Outliers: Int64Index([410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422,
            423, 424, 425, 426, 427, 428, 429],
           dtype='int64')
adult_outlier:
Outliers: Int64Index([689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701,
            702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714,
            715, 716, 717, 718, 719, 720, 721, 722],
           dtype='int64')
------------------------------------------------------------
Use Mahalanobis:
Test the method with noise:
infant_outlier:
[410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427
 428 429]
adult_outlier:
[689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706
 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722]
```

<div align="center">

|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  1 | 1 |
| Precision |1 | 1|
| Recall| 1 | 1 |
| F1 | 1 | 1|

</div>

#### Mds

```agsl
Use isolation tree:
Test the method with noise:
infant_outlier:
Outliers: Int64Index([  9,  26,  33,  47,  51,  67,  82, 145, 159, 167, 178, 202, 244,
            261, 272, 275, 281, 304, 308, 330],
           dtype='int64')
adult_outlier:
Outliers: Int64Index([ 18,  29,  93, 105, 107, 135, 166, 184, 188, 189, 200, 210, 212,
            224, 227, 230, 243, 266, 297, 307, 417, 419, 434, 435, 443, 445,
            447, 449, 465, 474, 617, 623, 628, 670],
           dtype='int64')
------------------------------------------------------------
Use Mahalanobis:
Test the method with noise:
infant_outlier:
[  0   9  10  26  33  76  82  99 159 178 202 244 272 275 281 288 330 331
 354 364]
adult_outlier:
[ 18  29  40  43  90 105 107 135 162 184 188 189 200 210 212 224 243 245
 266 301 373 419 434 435 437 447 449 465 556 574 617 623 624 628]
```

<div align="center">
|    | infant| adult |
| ---- | ---- | ---- |
| Accuracy|  0 | 0 |
| Precision |0 | 0|
| Recall| 0 | 0|
| F1 | 0 | 0 |
</div>

We can conclude that standard scaling and normalization scaling are very effective, but MDS scaling is too bad. 

## Conclusion

Based on the results, we found that both the Mahalanobis distance and Isolation Forest techniques were effective in identifying the added noise points accurately, without falsely flagging any of the true data points as outliers. These findings suggest that our outlier detection method using landmarks data is viable and can accurately identify outliers in complex datasets, even in the presence of noise. 
