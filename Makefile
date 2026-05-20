buildroot = /

python_version = 3
python_lookup_name = python$(python_version)
python = $(shell which $(python_lookup_name))

version := $(shell \
	$(python) -c \
	'from tiertune.version import __version__; print(__version__)'\
)

setup:
	poetry install --all-extras

check: setup
	# python flake tests
	poetry run flake8 --statistics -j auto --count tiertune
	poetry run flake8 --statistics -j auto --count test/unit

test: setup
	poetry run mypy tiertune
	poetry run bash -c 'pushd test/unit && pytest -n 5 \
		--doctest-modules --no-cov-on-fail --cov=tiertune \
		--cov-report=term-missing --cov-fail-under=100 \
		--cov-config .coveragerc'

black: setup
	poetry run black \
		--skip-string-normalization \
		--line-length 80 tiertune test/unit/

clean:
	rm -rf dist

build: clean check test
	# build the sdist source tarball
	poetry build --format=sdist
	# provide rpm source tarball
	mv dist/tiertune-${version}.tar.gz dist/python-tiertune.tar.gz
	# update rpm changelog using reference file
	helper/update_changelog.py --since package/python-tiertune.changes > \
		dist/python-tiertune.changes
	helper/update_changelog.py --file package/python-tiertune.changes >> \
		dist/python-tiertune.changes
	# update package version in spec file
	cat package/python-tiertune-spec-template | sed -e s'@%%VERSION@${version}@' \
		> dist/python-tiertune.spec
	# provide rpm rpmlintrc
	cp package/python-tiertune-rpmlintrc dist
