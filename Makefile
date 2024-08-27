.PHONE: help
help:
	@echo "build - build the package"
	@echo "upload - upload the package to PyPI"

.PHONY: build
build:
	source env/bin/activate
	python -m build --sdist
	python -m build --wheel

upload:
	source env/bin/activate
	twine check dist/*
	twine upload dist/*
