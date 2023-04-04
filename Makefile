data/300w.csv:
	@if [ ! -e "./data/300w.csv" ]; then \
		mkdir -p data; \
		cd data; curl -Lo 300w.csv https://github.com/ostadabbas/Infant-Facial-Landmark-Detection-and-Tracking/raw/master/data/300w/300w_valid.csv; \
	fi
data/infant.csv:
	@if [ ! -e "./data/infant.csv" ]; then \
		mkdir -p data; \
		cd data; curl -Lo infant.csv https://coe.northeastern.edu/Research/AClab/InfAnFace/labels.csv; \
	fi

data: data/300w.csv data/infant.csv

scale: data
	python -B ./src/scale.py

scale_plt:
	python -B ./src/scale_plt.py

scale_join:
	python -B ./src/scale_join.py

euclidean:
	python -B ./src/euclidean.py


ma_outlier_infant:
	python -B ./src/ma_infant.py

ma_outlier_adult:
	python -B ./src/ma_adult.py


if_outlier_adult:
	python -B ./src/isolation_forest_adult.py

if_outlier_infant:
	python -B ./src/isolation_forest_infant.py

pic:
	python -B ./src/pic.py

prelim_plots:
	python src/jh_prelim_plots.py

scatter:
	python src/scatter.py