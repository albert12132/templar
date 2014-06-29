
test-%: tests/test_%
	python3 -m unittest discover $< -p 'test_*.py'
