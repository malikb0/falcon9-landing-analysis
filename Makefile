PYTHON ?= python3

.PHONY: help install test nb report clean

help:
	@echo "make install  - install pinned dependencies"
	@echo "make test     - run the test suite"
	@echo "make nb       - execute the offline notebooks (03, 05, 07)"
	@echo "make report   - regenerate figures and the interactive map"
	@echo "make clean    - remove build output and caches"

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q tests

nb:
	jupyter nbconvert --to notebook --execute --inplace notebooks/03-data-wrangling.ipynb
	jupyter nbconvert --to notebook --execute --inplace notebooks/05-eda-visualization.ipynb
	jupyter nbconvert --to notebook --execute --inplace notebooks/07-ml-landing-prediction.ipynb

report:
	python scripts/make_figures.py

clean:
	rm -rf build .pytest_cache
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
