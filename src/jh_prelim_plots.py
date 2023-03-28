#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 20:31:24 2022

@author: jhautala
"""

from util import meta_cache
from util.plot import plot_image
from util.pre import rotate

save_fig = False

# anno_img = meta_cache.get_image(17, baby=True)
# outlier
arr = [707, 736, 782, 798, 802, 834, 835, 837, 843, 868, 935, 940, 951, 1023, 1029, 1048, 1064, 1066, 1092, 1095]
# not outlier
arr1 = [694, 695, 696, 697, 698]

for i in arr1:
    anno_img = meta_cache.get_image(i-2)

    for annotate in ['scatternum']:
        plot_image(
            anno_img,
            annotate=annotate,
            save_fig=save_fig,
        )
'''
for (row_id, annotate) in [
        (4, None),
        (1, 'scatter'),
        (0, 'splinelabel')
]:
    plot_image(
        rotate(meta_cache.get_image(row_id, baby=True)),
        annotate=annotate,
        cross=True,
        save_fig=save_fig,
    )
    '''
