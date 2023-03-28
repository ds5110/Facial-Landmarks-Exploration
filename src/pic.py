import pandas as pd
import os
from PIL import Image
'''
# read csv
df = pd.read_csv("outcome/outlier_selection/labels.csv")

# filter
selected_rows = df.loc[df.index.isin([16, 45, 91, 107, 111, 143, 144, 146, 152, 177, 244, 249, 260, 332, 338, 341, 357, 373, 375, 401, 404])]

# save result in the file
selected_rows.to_csv("outcome/outlier_selection/selected_data.csv", index=False)
'''
# 读取csv文件，假设文件名为data.csv
df = pd.read_csv('data/11.csv')

# 遍历每一行，并根据image-set和filename列构造出完整的文件路径
for _, row in df.iterrows():
    image_set = row['image-set']
    filename = row['filename']
    file_path = os.path.join("data", "images", image_set, filename)
    img = Image.open(file_path)
    # 显示图片
    img.show()
'''
    with open(file_path, 'r') as f:
        content = f.read()
'''