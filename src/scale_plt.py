import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

idx = [0, 4, 8, 16]
id_cols = ['image_name', 'baby', 'scale_type']

# Combine data and split them to infant and adult.
all_raw = pd.read_csv('./outcome/scale/all_raw.csv')
all_raw_scale = pd.read_csv('./outcome/scale/all_raw_scale.csv')
all_raw['scale_type'] = 'original'
all_raw_infant = all_raw[all_raw['baby'] == 1].iloc[idx]
all_raw_adult = all_raw[all_raw['baby'] == 0].iloc[idx]
infant_names = all_raw_infant['image_name']
adult_names = all_raw_adult['image_name']

all_raw_scale_infant = all_raw_scale[all_raw_scale['image_name'].isin(infant_names)]
all_raw_scale_adult = all_raw_scale[all_raw_scale['image_name'].isin(adult_names)]


# plot the dataframe by its scale_type.
def plot(df_list, col_order, title, path):
    combined_df = pd.concat(df_list)
    combined_df['image_name'] = combined_df['image_name'].str[-10:]
    melted = pd.melt(combined_df, id_vars=id_cols, var_name='col_name', value_name='coord_value')
    melted['coord_type'] = melted['col_name'].str[0]
    melted['coord_num'] = melted['col_name'].str[1:]
    melted['coord_num'] = melted['coord_num'].astype(int)
    pivoted = melted.pivot(index=id_cols + ['coord_num'], columns='coord_type', values='coord_value')
    merged_data = pivoted.reset_index()

    g = sns.FacetGrid(merged_data, row='image_name', col='scale_type', margin_titles=True, sharex=False, sharey=False,
                      col_order=col_order)
    g = g.map(sns.scatterplot, 'x', 'y')

    g.fig.suptitle(title, y=1.08)
    g.set_axis_labels("X-axis", "Y-axis")
    g.set_titles(template=title, row_template="")
    plt.savefig(path)
    plt.show()


plot([all_raw_scale_infant, all_raw_infant], ['original', 'mds', 'normalized', 'standard'],
     "Infant Scale Comparison Plots", "./outcome/scale/raw_infant.png")
plot([all_raw_scale_adult, all_raw_adult], ['original', 'mds', 'normalized', 'standard'],
     "Adult Scale Comparison Plots", "./outcome/scale/raw_adult.png")

center_raw = pd.read_csv('./outcome/scale/center_by_nose_raw.csv')
center_scale = pd.read_csv('./outcome/scale/center_scale.csv')
prev_df = pd.read_csv('./outcome/prev/merged_landmarks.csv')


# plot the center data. Merged the data from previous project and the original data for comparison.
def plot_center(names, title, path):
    center_raw_plt = center_raw[center_raw['image_name'].isin(names)].copy()
    center_raw_plt['scale_type'] = 'original'
    center_scale_plt = center_scale[center_scale['image_name'].isin(names)]
    prev_df_plt = prev_df[prev_df['image_name'].isin(names)]

    def rename_cols(col_name):
        if col_name.startswith('norm-'):
            return col_name[5:]
        else:
            return col_name

    desired_names = ['baby', 'image_name'] + [f'norm-x{i}' for i in range(68)] + [f'norm-y{i}' for i in range(68)]
    prev_df_plt = prev_df_plt.loc[:, desired_names]
    prev_df_plt = prev_df_plt.rename(columns=rename_cols)
    prev_df_plt['scale_type'] = 'Previous Project'
    plot([center_raw_plt, center_scale_plt, prev_df_plt],
         ['original', 'Previous Project', 'mds', 'normalized', 'standard'],
         title, path)


plot_center(infant_names, 'Infant Center Scale Comparison Plots', './outcome/scale/center_infant.png')
plot_center(adult_names, 'Adult Center Scale Comparison Plots', './outcome/scale/center_adult.png')

rotated_raw = pd.read_csv('./outcome/scale/rotated_raw.csv')
rotated_scale = pd.read_csv('./outcome/scale/rotated_scale.csv')


# plot the rotation data. Merged the data from previous project and the original data for comparison.
def plot_rotated(names, title, path):
    rotated_raw_plt = rotated_raw[rotated_raw['image_name'].isin(names)].copy()
    rotated_raw_plt['scale_type'] = 'original'
    rotated_scale_plt = rotated_scale[rotated_scale['image_name'].isin(names)]
    prev_df_plt = prev_df[prev_df['image_name'].isin(names)]

    def rename_cols(col_name):
        if col_name.startswith('norm_cenrot-'):
            return col_name[12:]
        else:
            return col_name

    desired_names = ['baby', 'image_name'] + [f'norm_cenrot-x{i}' for i in range(68)] + \
                    [f'norm_cenrot-y{i}' for i in range(68)]
    prev_df_plt = prev_df_plt.loc[:, desired_names]
    prev_df_plt = prev_df_plt.rename(columns=rename_cols)
    prev_df_plt['scale_type'] = 'Previous Project'
    plot([rotated_raw_plt, rotated_scale_plt, prev_df_plt],
         ['original', 'Previous Project', 'mds', 'normalized', 'standard'],
         title, path)


plot_rotated(infant_names, 'Infant Rotated Scale Comparison Plots', './outcome/scale/rotated_infant.png')
plot_rotated(adult_names, 'Adult Rotated Scale Comparison Plots', './outcome/scale/rotated_adult.png')
