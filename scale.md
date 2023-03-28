# Investigating the Best Way to Scale Landmarks

## Introduction

The scaling of landmarks is an important step in our image processing tasks. In this part of our project, three
different scaling approaches were used, including standardization, normalization by face bounding box, and
Multidimensional scaling. The objective of this study was to find the best way to scale landmarks that would keep the
range of landmarks within a similar distance while maintaining constant relative distances between landmarks. The
Min-Max Scale and Unit Vector Scale approaches were also considered but were found unsuitable for the given usage
scenario.

## Approach

- Standardization: Using the `sklearn.preprocessing.StandardScaler` to normalize the landmarks of each image separately.
- Normalization by face bounding box: Normalized x coordinate by dividing with the x-axis range in landmarks, and y
  coordinate by dividing with the y-axis range.
- MDS: The Multidimensional scaling approach used `sklearn.manifold.MDS` to perform the scaling on
  the landmarks of each image.

**Infant Comparison**
![infant](./outcome/scale/infant.png)
**Adult Comparison**
![adult](./outcome/scale/adult.png)

## Conclusion

As we can see, though standardization and normalization use different range as the denominator, they have similar views.
And The MDS would rotate the view in some degrees. We would like to compare it with the scale method that previous
project applied and check the difference between them.
