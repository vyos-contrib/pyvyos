.PHONY: help
help:
	@echo "build - build the package"
	@echo "upload - upload the package to PyPI"

.PHONY: build
build:
	env/bin/python -m build --sdist
	env/bin/python -m build --wheel

.PHONY: upload
upload:
	env/bin/python -m twine check dist/*
	env/bin/python -m twine upload dist/*
