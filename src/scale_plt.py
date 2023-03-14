import matplotlib.pyplot as plt
import utils
import seaborn as sns
import numpy as np
import pandas as pd

infant, adult, mds_infant, mds_adult, norm_infant, norm_adult, std_infant, std_adult = utils.get_all_scale_data()

idx = [0, 4, 8, 16]
# Infant
# infant['type'] = 'original'
# infant.reset_index(inplace=True)
# mds_infant['type'] = 'mds'
# mds_infant.reset_index(inplace=True)
# norm_infant['type'] = 'normal'
# norm_infant.reset_index(inplace=True)
# std_infant['type'] = 'standard'
# std_infant.reset_index(inplace=True)
# infant_id_cols = ['type', 'index', 'image-set', 'filename', 'partition', 'subpartition', 'turned', 'occluded',
#                   'expressive', 'tilted']
# combined_df = pd.concat([infant.loc[idx], mds_infant.loc[idx], norm_infant.loc[idx], std_infant.loc[idx]])
# melted = pd.melt(combined_df, id_vars=infant_id_cols, var_name='col_name', value_name='coord_value')
# melted['coord_type'] = melted['col_name'].str[3]
# melted['coord_num'] = melted['col_name'].str[4:]
# melted['coord_num'] = melted['coord_num'].astype(int)
# pivoted = melted.pivot(index=infant_id_cols + ['coord_num'], columns='coord_type', values='coord_value')
# merged_data = pivoted.reset_index()
#
# g = sns.FacetGrid(merged_data, row='index', col='type', margin_titles=True, sharex=False, sharey=False,
#                   col_order=['original', 'mds', 'normal', 'standard'])
# g = g.map(sns.scatterplot, 'x', 'y')
#
# g.fig.suptitle("Infant Scale Comparison Plots", y=1.08)
# g.set_axis_labels("X-axis", "Y-axis")
#
# plt.savefig("./outcome/scale/infant.png")
# plt.show()

# Adult
adult['type'] = 'original'
adult.reset_index(inplace=True)
mds_adult['type'] = 'mds'
mds_adult.reset_index(inplace=True)
norm_adult['type'] = 'normal'
norm_adult.reset_index(inplace=True)
std_adult['type'] = 'standard'
std_adult.reset_index(inplace=True)
combined_df = pd.concat([adult.loc[idx], mds_adult.loc[idx], norm_adult.loc[idx], std_adult.loc[idx]])
adult_id_cols = ['image_name', 'type', 'index', 'scale', 'center_w', 'center_h']
melted = pd.melt(combined_df, id_vars=adult_id_cols, var_name='col_name', value_name='coord_value')
# format: original_0_x
melted['coord_type'] = melted['col_name'].str.split('_', expand=True)[2]
melted['coord_num'] = melted['col_name'].str.split('_', expand=True)[1]
melted['coord_num'] = melted['coord_num'].astype(int)
pivoted = melted.pivot(index=adult_id_cols + ['coord_num'], columns='coord_type', values='coord_value')
merged_data = pivoted.reset_index()

g = sns.FacetGrid(merged_data, row='index', col='type', margin_titles=True, sharex=False, sharey=False,
                  col_order=['original', 'mds', 'normal', 'standard'])
g = g.map(sns.scatterplot, 'x', 'y')

g.fig.suptitle("Adult Scale Comparison Plots", y=1.08)
g.set_axis_labels("X-axis", "Y-axis")

plt.savefig("./outcome/scale/adult.png")
plt.show()
