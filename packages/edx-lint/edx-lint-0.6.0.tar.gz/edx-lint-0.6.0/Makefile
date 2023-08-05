# Makefile for edx-lint

.PHONY: default test

default: test

test:
	tox -e py27,py35,coverage

pylint:
	tox -e pylint

clean:
	-rm -rf *.egg-info
	-find . -name '__pycache__' -prune -exec rm -rf "{}" \;
	-find . -name '*.pyc' -delete
	-rm -f MANIFEST
	-rm -rf .coverage .coverage.* htmlcov
	-rm -rf .tox

requirements:
	pip install -r dev-requirements.txt
