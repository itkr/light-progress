.PHONY: deploy
deploy: build
	twine upload dist/*

.PHONY: test-deploy
test-deploy: build
	twine upload -r pypitest dist/*

.PHONY: build
build:
	# python setup.py sdist bdist_wheel
	python setup.py sdist

test-install:
	pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple light-progress
