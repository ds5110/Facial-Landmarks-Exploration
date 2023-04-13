## Introduction

This documentation provides an overview of the project structure and the usage of each file. The goal is to provide
clear and concise information on the project, make the code understandable, and share our thought process for each step.

## Project Structure

#### Environment

The `Makefile` contains all the commands for the project, and all of the code is located in the `src` folder.

To set up the environment, run `conda env create -f environment.yml` and activate it
with `conda activate DS5110-faces-extend`. After that, you can run the scale functions.

#### Datasource

The original infants' and adults' landmarks data is located in the `data` folder, and it can be accessed directly by
running `make data`. Another important part of our analysis is the data from a previous project, which includes
coordinates that have been scaled and rotated. As this is not a public project, the data file is located
in `outcome/prev/merged_landmarks.csv`.

#### Makefile

The `Makefile` serves as the entry point for the entire project, and all of the completed functions are located there.
It contains four parts:

- `data`: Used for downloading the original data from Michael Wan's study.
- `scale`: Used for applying different scaling functions to the original data and comparing it with
  the `merged_landmarks` from the previous project.
- `outlier`: Used for detecting different functions that can be used for detecting outliers in the landmarks.
- `TODO`: Feature selections.

### File

##### scale.py

The `scale.py` file is used for applying scaling functions to the original data.

Before applying these scaling functions, we need to merge the data into a dataframe with the same columns for landmarks
and other columns containing properties we care about. We add a `baby` column to mark whether the data belongs to the
baby or adult dataframe, and we combine the image-set and filename in the infant dataset to get a similar `image_name`
in the adult dataset.

We then subtract all coordinates by the specified `x33` and `y33`, which are the coordinates of the nose. This moves all
the centers in the image to `(0,0)` in the new dataframe. The formula is:

$$
sx_i=x_i - x_{33}\\
sy_i=y_i - y_{33}\\
$$

After that, we rotate the image to ensure that all the images are in the same posture. This is done using the same
rotation method as in the previous project. The function is located in `rotate_calculator.py`, which will be introduced
later.

We now have three datasets: `all_raw_df`, which contains the original data; `center_by_nose_df`, which has the data
aligned to the center by the nose; and `rotated_df`, which has the data rotated to the same orientation. In the
following functions, we apply these datasets to different scaling functions. Before applying them, we would like to
introduce the scaling function used in the previous project.

The previous project had two kinds of data as a result. They combined all the data, added a `baby` column, and made the
nose the center. They then rotated the data using the same method as in `rotate_calculator.py`. After that, they scaled
the data using this formula:

$$
sx_i=(x_i - x_{33})/range\\
sy_i=(y_i - y_{33})/range\\
range = (max(X \cup Y) - min(X \cup Y))\\
$$

This was the final set of landmarks used in all calculations.

We tried three scaling functions after center alignment and rotation:

- `standardize_original`: This function applies `StandardScaler` to the dataset. The formula is:

$$
sx_i = \frac{x_i - \mu_x}{\sigma_x}\\
sy_i = \frac{y_i - \mu_y}{\sigma_y}\\
$$

- `normalize_by_face_bounding_box`: This function normalizes the data in a similar way to the previous project:

$$
sx_i=(x_i - x_{33})/range_x\\
sy_i=(y_i - y_{33})/range_y\\
range_x = max(X) - min(X)\\
range_y = max(Y) - min(Y)\\
$$

- `normalize_coords_by_face_bounding_box`: This function is the actual calculation function, and the above function
  combines the results into an appropriate dataframe.

- `scale_mds`: This function applies `mds` scaling to the landmarks.

    - `mds_by_coordinates`: This function applies `mds` scaling in the required format, and the above function
      transforms the result into an appropriate dataframe.

- `scale_all`: This function scales the dataframe using the three methods above, marks the scale type being used, and
  concatenates them together.

After that, we scale all the dataframes we obtained earlier (`all_raw_df`, `center_by_nose_df`, and `rotated_df`) using
the `scale_all` function. We output these dataframes to the `outcome/scale` folder, which is prepared for future
analysis. The mission of `scale.py` is completed.

##### rotate_calculator.py

This function is used to calculate the angles and apply them to the dataframe. The steps are:

1. **Select Landmark Groups**: Choose two groups of landmarks for rotation calculation: `[36, 45], [39, 42]` (outer and
   inner eye corners) and `[37, 44], [38, 43], [40, 47], [41, 46]` (upper and lower eyelids). These two groups are
   calculated separately. The two groups are defined in the `default_syms` variable.

2. **Calculate the Angle**: The angle is determined using the following formula:

   ```
   xx = right_x - left_x
   yy = left_y - right_y (since the y coordinate is from up to down)
   hypots = np.hypot(xx, yy)
   weight = np.sum(hypots)
   x = np.sum(xx * hypots) / weight
   y = np.sum(yy * hypots) / weight
   angle = np.arctan(y / x)
   ```

   The code for this calculation can be found in the `_get_yaw` function.

3. **Combine the Angles**:

   ```
   weights = [len(groups) for all_group]
   angle = np.sum(angles * weights) / np.sum(weights)
   ```

   The code for this calculation can be found in the `get_angle` function.

4. **Compute New Coordinates**: Calculate the new coordinates after applying the rotation:

   ```
   rotx = np.array([[cos, sin], [-sin, cos]])
   coords = coords @ rotx
   ```

   The code for this calculation can be found in the `rotate` function.

##### utils.py

This file stores some common functions that are used.

`reshape_to_2d`: Reshapes the dataframe into a 3d array.

##### scale_plt.py

This function is used to plot the distribution of the landmarks, obtain a visualization of them, and find some insights
from them. In the first part, we read the data from the raw file generated in `scale.py`, combine them together, and
split them into infants and adults.

The `plot` function is used to plot the dataframe as a grid image. The columns of the grid represent the scale type, and
the rows represent some fixed indices, so we can obtain a direct understanding of the effect of each scaling method.

After that, we plot the raw data and the data that has been aligned to the center. The `plot_center` function is used to
merge the data from the previous project and the original data for comparison.

After plotting the center data, we read the rotated data and use the `plot_rotated` function to draw an image.

Finally, we obtain six images of different data and scaling methods that we used, providing us with a direct
visualization. You can find them in the `outcome/scale/` folder.