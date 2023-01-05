.PHONY: check remove-build convert-readme build deploy test-deploy test-install

check:
	python check.py

remove-build:
	rm -f README.rst
	rm -rf build/ dist/ light_progress.egg-info/

convert-readme:
	docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/latex README.md -o README.rst

build: remove-build convert-readme
	python setup.py sdist bdist_wheel
	# python setup.py sdist

deploy: build
	twine upload dist/*

test-deploy: build
	twine upload -r pypitest dist/*

test-install:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple light-progress
