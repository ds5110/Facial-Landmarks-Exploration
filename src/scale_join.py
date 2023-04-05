import pandas as pd
import utils

infant, adult, mds_infant_df, mds_adult_df, normalized_infant_df, normalized_adult_df, standard_infant_df, standard_adult_df = utils.get_all_scale_data()

# Merge the adult and infant dataframes for each scale type
mds_infant_df['image_name'] = mds_infant_df[['image-set', 'filename']].agg('/'.join, axis=1)
mds_merged = pd.merge(mds_adult_df, mds_infant_df, how='outer', on='image_name')
mds_merged['scale_type'] = 'mds'
normalized_infant_df['image_name'] = normalized_infant_df[['image-set', 'filename']].agg('/'.join, axis=1)
normalized_merged = pd.merge(normalized_adult_df, normalized_infant_df, how='outer', on='image_name')
normalized_merged['scale_type'] = 'normalized'
standard_infant_df['image_name'] = standard_infant_df[['image-set', 'filename']].agg('/'.join, axis=1)
standard_merged = pd.merge(standard_adult_df, standard_infant_df, how='outer', on='image_name')
standard_merged['scale_type'] = 'standard'

# Combine the three merged dataframes into one
merged = pd.concat([mds_merged, normalized_merged, standard_merged])

# Create a new dataframe with the desired output format
output_df = pd.DataFrame(columns=['image_name'] + [f'x{i}' for i in range(68)] + [f'y{i}' for i in range(68)] +
                                 ['baby', 'scale_type'])

# Loop through the merged dataframe and extract the required data
for _, row in merged.iterrows():
    image_name = row['image_name']
    scale_type = row['scale_type']
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
    output_row = [image_name] + x_values + y_values + [baby, scale_type]
    output_df.loc[len(output_df)] = output_row

# Save the output dataframe to a csv file
output_df.to_csv('./outcome/scale/scale.csv', index=False)
