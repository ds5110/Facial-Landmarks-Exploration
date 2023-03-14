import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS
import numpy as np

infant = pd.read_csv('./data/infant.csv')
adult = pd.read_csv('./data/300w.csv')


def standardize_original():
    standard_infant = infant.copy()
    infant_coords = [col for col in standard_infant.columns if col.startswith('gt-')]

    scaler = StandardScaler()
    standard_infant[infant_coords] = scaler.fit_transform(standard_infant[infant_coords])
    standard_infant.to_csv('./outcome/scale/standard_infant.csv', index=False)

    standard_adult = adult.copy()
    adult_coords = [col for col in adult.columns if col.startswith('original_')]
    standard_adult[adult_coords] = scaler.fit_transform(adult[adult_coords])
    standard_adult.to_csv('./outcome/scale/standard_adult.csv', index=False)


def normalize_coords_by_face_bounding_box(x_coords, y_coords):
    # Calculate the range of x and y values for each row
    x_range = x_coords.max(axis=1) - x_coords.min(axis=1)
    y_range = y_coords.max(axis=1) - y_coords.min(axis=1)

    # Divide each row of x and y coordinates by the respective range
    x_normalized = x_coords.div(x_range, axis=0)
    y_normalized = y_coords.div(y_range, axis=0)

    # Combine the normalized x and y coordinates back into a single DataFrame
    normalized_df = pd.concat([x_normalized, y_normalized], axis=1)
    return normalized_df


def normalize_by_face_bounding_box():
    x_cols = [col for col in infant.columns if 'gt-x' in col]
    y_cols = [col for col in infant.columns if 'gt-y' in col]
    x_coords = infant[x_cols]
    y_coords = infant[y_cols]
    normalized_infant = infant.copy()
    infant_result = normalize_coords_by_face_bounding_box(x_coords, y_coords)
    normalized_infant[x_cols + y_cols] = infant_result
    normalized_infant.to_csv('./outcome/scale/normalized_infant.csv', index=False)

    x_cols = [col for col in adult.columns if 'x' in col]
    y_cols = [col for col in adult.columns if 'y' in col]
    x_coords = adult[x_cols]
    y_coords = adult[y_cols]
    normalized_adult = adult.copy()
    adult_result = normalize_coords_by_face_bounding_box(x_coords, y_coords)
    normalized_adult[x_cols + y_cols] = adult_result
    normalized_adult.to_csv('./outcome/scale/normalized_adult.csv', index=False)


def mds_by_coordinates(x_coords, y_coords):
    num_rows = x_coords.shape[0]
    infant_reshaped = np.zeros((num_rows, 68, 2))
    infant_reshaped[:, :, 0] = x_coords
    infant_reshaped[:, :, 1] = y_coords
    num_rows, num_landmarks, num_dimensions = infant_reshaped.shape
    # Initialize an empty array to store the MDS results
    mds_results = np.zeros((num_rows, num_landmarks, num_dimensions))

    # Iterate over each row of the landmark data and perform MDS
    for i in range(num_rows):
        mds = MDS(n_components=num_dimensions)
        mds_transformed = mds.fit_transform(infant_reshaped[i])
        mds_results[i] = mds_transformed
    return mds_results


def scale_mds():
    x_cols = [col for col in infant.columns if 'gt-x' in col]
    y_cols = [col for col in infant.columns if 'gt-y' in col]
    x_coords = infant[x_cols]
    y_coords = infant[y_cols]
    mds_results = mds_by_coordinates(x_coords, y_coords)
    mds_infant = infant.copy()
    for i in range(68):
        mds_infant['gt-x' + str(i)] = mds_results[:, i, 0]
        mds_infant['gt-y' + str(i)] = mds_results[:, i, 1]
    mds_infant.to_csv('./outcome/scale/mds_infant.csv', index=False)

    x_cols = [col for col in adult.columns if 'x' in col]
    y_cols = [col for col in adult.columns if 'y' in col]
    x_coords = adult[x_cols]
    y_coords = adult[y_cols]
    mds_results = mds_by_coordinates(x_coords, y_coords)
    mds_adult = adult.copy()
    for i in range(68):
        mds_adult['original_' + str(i) + "_x"] = mds_results[:, i, 0]
        mds_adult['original_' + str(i) + '_y'] = mds_results[:, i, 1]
    mds_adult.to_csv('./outcome/scale/mds_adult.csv', index=False)


standardize_original()
normalize_by_face_bounding_box()
scale_mds()
