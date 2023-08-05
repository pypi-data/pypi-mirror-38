help:
	@echo "The following make targets are available:"
	@echo "dev	install all deps for dev env"
	@echo "docs	create pydocs for all relveant modules"
	@echo "test	run all tests with coverage"

clean:
	rm -rf dist/*

dev:
	pip install coverage
	pip install codecov
	pip install pylint
	pip install twine
	pip install -e .

docs:
	$(MAKE) -C docs html

lint-comment:
	! find . -name '*.py' -and -not -path './venv/*' | xargs grep -nE '#.*(todo|xxx|fixme|n[oO][tT][eE]:|Note:|nopep8\s*$)'

lint-pycodestyle:
	pycodestyle --exclude=venv --ignore=E266,E501,W503 .

lint-pylint:
	find . -name '*.py' -and -not -path './venv/*' | sort | tee /dev/tty | xargs pylint -j 6 -d E0602,W0511,R0205,C0111,C0103,C0301,R0913,R0902,R0903

VERSION=`echo "import accern;print(accern.__version__)" | python 2>/dev/null`

publish:
	@git diff --exit-code 2>&1 >/dev/null && git diff --cached --exit-code 2>&1 >/dev/null || (echo "working copy is not clean" && exit 1)
	@test -z `git ls-files --other --exclude-standard --directory` || (echo "there are untracked files" && exit 1)
	@test `git rev-parse --abbrev-ref HEAD` = "master" || (echo "not on master" && exit 1)
	python setup.py sdist bdist_wheel
	twine upload dist/Accern-$(VERSION)-py2.py3-none-any.whl dist/Accern-$(VERSION).tar.gz
	git tag "v$(VERSION)"
	git push origin "v$(VERSION)"
	@echo "succesfully deployed $(VERSION)"

test:
	coverage run -m unittest discover
	coverage html
