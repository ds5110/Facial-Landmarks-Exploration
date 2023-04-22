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

scale_data: data
	python -B ./src/scale.py

scale_plt:
	python -B ./src/scale_plt.py

scale: scale_data scale_plt

euclidean_data:
	python -B ./src/euclidean.py

euclidean_data_scale:
	python -B ./src/euclidean.py scale

euclidean: euclidean_data euclidean_data_scale

scatter:
	python src/scatter.py

outlier:
	python src/outlier.py

outlier_scale:
	python src/outlier_scale.py

outlier_detection: scatter outlier outlier_scale

# The following two commands reproduce feature selection results
# Can be very time-consuming up to tens of minitues
feature_data:
	python -u -B src/feature_selection.py

feature_data_scale:
	python -u -B src/feature_selection.py scale

feature_plots:
	python -u -B src/feature_selection_plots.py

feature_plots_scale:
	python -u -B src/feature_selection_plots.py scale

feature: feature_data feature_data_scale feature_plots feature_plots_scale