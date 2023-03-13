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
