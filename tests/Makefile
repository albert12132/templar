
all:
	python3 -m unittest discover -p '*tests.py'

%: %_tests
	python3 -m unittest discover $< -p '*tests.py'
