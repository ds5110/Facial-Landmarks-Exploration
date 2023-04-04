import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS
import numpy as np
import utils
from rotate_calculator import rotate

infant = pd.read_csv('./data/infant.csv')
adult = pd.read_csv('./data/300w.csv')
nose = 33

infant_tmp = infant.copy()
infant_tmp['image_name'] = infant_tmp[['image-set', 'filename']].agg('/'.join, axis=1)
merged_df = pd.merge(adult, infant_tmp, how='outer', on='image_name')
all_raw_df = pd.DataFrame(columns=['image_name', 'baby'] + [f'x{i}' for i in range(68)] + [f'y{i}' for i in range(68)])
for _, row in merged_df.iterrows():
    image_name = row['image_name']
    if pd.notna(row['image-set']):
        # This is an infant record
        baby = 1
        x_cols = [f'gt-x{i}' for i in range(68)]
        y_cols = [f'gt-y{i}' for i in range(68)]
    else:
        # This is an adult record
        baby = 0
        x_cols = [f'original_{i}_x' for i in range(68)]
        y_cols = [f'original_{i}_y' for i in range(68)]

    # Extract the x and y coordinates and add them to the output dataframe
    x_values = row[x_cols].tolist()
    y_values = row[y_cols].tolist()
    output_row = [image_name, baby] + x_values + y_values
    all_raw_df.loc[len(all_raw_df)] = output_row

x_cols = [f'x{i}' for i in range(68)]
y_cols = [f'y{i}' for i in range(68)]
center_by_nose_df = all_raw_df.copy()
center_by_nose_df[x_cols] = center_by_nose_df[x_cols].subtract(center_by_nose_df['x' + str(nose)], axis=0)
center_by_nose_df[y_cols] = center_by_nose_df[y_cols].subtract(center_by_nose_df['y' + str(nose)], axis=0)

rotated_df = center_by_nose_df.copy()
rotated_df.apply(lambda row: rotate(row, x_cols, y_cols), axis=1)


def standardize_original(df, cols):
    scaler = StandardScaler()
    df = df.copy()
    df[cols] = df[cols].apply(
        lambda x: scaler.fit_transform(x.values.reshape(68, 2)).reshape(136), axis=1, result_type='expand')
    return df


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


def normalize_by_face_bounding_box(df, x_cols, y_cols):
    df = df.copy()
    res = normalize_coords_by_face_bounding_box(df[x_cols], df[y_cols])
    df[x_cols + y_cols] = res
    return df


def mds_by_coordinates(df, x_cols, y_cols):
    infant_reshaped = utils.reshape_to_2d(df, x_cols, y_cols)
    num_rows, num_landmarks, num_dimensions = infant_reshaped.shape
    mds_results = np.zeros((num_rows, num_landmarks, num_dimensions))
    for i in range(num_rows):
        mds = MDS(n_components=num_dimensions)
        mds_transformed = mds.fit_transform(infant_reshaped[i])
        mds_results[i] = mds_transformed
    return mds_results


def scale_mds(df, x_cols, y_cols):
    mds_results = mds_by_coordinates(df, x_cols, y_cols)
    df = df.copy()
    df[x_cols] = mds_results[:, :, 0]
    df[y_cols] = mds_results[:, :, 1]
    return df


def scale_all(df, x_cols, y_cols):
    standardize_df = standardize_original(df, x_cols + y_cols)
    standardize_df['scale_type'] = 'standard'
    normalized_df = normalize_by_face_bounding_box(df, x_cols, y_cols)
    normalized_df['scale_type'] = 'normalized'
    mds_df = scale_mds(df, x_cols, y_cols)
    mds_df['scale_type'] = 'mds'
    merged = pd.concat([standardize_df, normalized_df, mds_df])
    return merged


all_raw_scale = scale_all(all_raw_df, x_cols, y_cols)
center_scale = scale_all(center_by_nose_df, x_cols, y_cols)
rotated_scale = scale_all(rotated_df, x_cols, y_cols)
all_raw_df.to_csv('./outcome/scale/all_raw.csv', index=False)
center_by_nose_df.to_csv('./outcome/scale/center_by_nose_raw.csv', index=False)
rotated_df.to_csv('./outcome/scale/rotated_raw.csv', index=False)
all_raw_scale.to_csv('./outcome/scale/all_raw_scale.csv', index=False)
center_scale.to_csv('./outcome/scale/center_scale.csv', index=False)
rotated_scale.to_csv('./outcome/scale/rotated_scale.csv', index=False)
