.PHONY: format check

format:
	black meter
	isort meter

check:
	echo 'Checking code format with black...'
	black --check meter
	echo 'Checking import order...'
	isort --check meter
	echo 'Running flake8...'
	flake8 meter --config=.flake8
	echo 'Running mypy...'
	mypy meter --config=mypy.ini

