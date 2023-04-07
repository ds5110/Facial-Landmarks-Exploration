# Investigating the Best Way to Select Outliers

## Introduction

Calculate the mean, median, standard deviation, and range of the variables, and plot boxplot for each variable in the data to gain insights into the distribution.


## Result
The noise index is 411-430  690-723  

Ma
```agsl
infant:  
[10  80 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429]
adult:
[21 284 624 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722]
```

```agsl
infant_outlier:
[ 3 10  12  13  35  38  64  68  80  81  89  90  99 183 205 239 258 285 288 335 364]
adult_outlier:
[ 15  21  28  40 109 142 167 168 180 226 248 261 269 277 284 296 331 335 339 356 368 369 371 382 395 464 566 574 588 594 624 625 657 665 681]
```

Isolation:  
```agsl
Test the method with noise:
infant_outlier:
Outliers: Int64Index([ 10,  13, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420,
421, 422, 423, 424, 425, 426, 427, 428, 429], dtype='int64')
adult_outlier:

Outliers: Int64Index([296, 371, 665, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698,
699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711,
712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722],dtype='int64')
```

```agsl
Data:
infant_outlier:
Outliers: Int64Index([  3,  10,  11,  13,  31,  32,  38,  68,  69,  80,  81,  88,  90,
98,  99, 203, 205, 239, 253, 335, 364],dtype='int64')
adult_outlier:
Outliers: Int64Index([ 15,  21,  28,  40,  73,  86, 109, 142, 145, 150, 172, 200, 214,
226, 269, 296, 317, 335, 336, 339, 344, 365, 371, 422, 461, 464,
484, 510, 582, 626, 647, 657, 665, 667, 681], dtype='int64')
```


## Conclusion


