import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS
import numpy as np
import utils

infant = pd.read_csv('./data/infant.csv')
adult = pd.read_csv('./data/300w.csv')

infant_cols, infant_x_cols, infant_y_cols = utils.get_infant_cols(infant)
adult_cols, adult_x_cols, adult_y_cols = utils.get_adult_cols(adult)


def standardize_original():
    scaler = StandardScaler()

    standard_infant = infant.copy()
    # standard_infant[infant_cols] = scaler.fit_transform(standard_infant[infant_cols])

    standard_infant[infant_cols] = standard_infant[infant_cols].apply(
        lambda x: scaler.fit_transform(x.values.reshape(68, 2)).reshape(136), axis=1, result_type='expand')

    standard_infant.to_csv('./outcome/scale/standard_infant.csv', index=False)

    standard_adult = adult.copy()
    # standard_adult[adult_cols] = scaler.fit_transform(adult[adult_cols])
    standard_adult[adult_cols] = standard_adult[adult_cols].apply(
        lambda x: scaler.fit_transform(x.values.reshape(68, 2)).reshape(136), axis=1, result_type='expand')
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
    normalized_infant = infant.copy()
    infant_result = normalize_coords_by_face_bounding_box(infant[infant_x_cols], infant[infant_y_cols])
    normalized_infant[infant_cols] = infant_result
    normalized_infant.to_csv('./outcome/scale/normalized_infant.csv', index=False)

    normalized_adult = adult.copy()
    adult_result = normalize_coords_by_face_bounding_box(adult[adult_x_cols], adult[adult_y_cols])
    normalized_adult[adult_cols] = adult_result
    normalized_adult.to_csv('./outcome/scale/normalized_adult.csv', index=False)


def mds_by_coordinates(df, x_cols, y_cols):
    infant_reshaped = utils.reshape_to_2d(df, x_cols, y_cols)
    num_rows, num_landmarks, num_dimensions = infant_reshaped.shape
    mds_results = np.zeros((num_rows, num_landmarks, num_dimensions))
    for i in range(num_rows):
        mds = MDS(n_components=num_dimensions)
        mds_transformed = mds.fit_transform(infant_reshaped[i])
        mds_results[i] = mds_transformed
    return mds_results


def scale_mds():
    mds_results = mds_by_coordinates(infant, infant_x_cols, infant_y_cols)
    mds_infant = infant.copy()
    for i in range(68):
        mds_infant['gt-x' + str(i)] = mds_results[:, i, 0]
        mds_infant['gt-y' + str(i)] = mds_results[:, i, 1]
    mds_infant.to_csv('./outcome/scale/mds_infant.csv', index=False)

    mds_results = mds_by_coordinates(adult, adult_x_cols, adult_y_cols)
    mds_adult = adult.copy()
    for i in range(68):
        mds_adult['original_' + str(i) + "_x"] = mds_results[:, i, 0]
        mds_adult['original_' + str(i) + '_y'] = mds_results[:, i, 1]
    mds_adult.to_csv('./outcome/scale/mds_adult.csv', index=False)


standardize_original()
normalize_by_face_bounding_box()
scale_mds()
