PY3 = python3
PIP3 = pip3
PYPY3 = pypy3

default: install

clean:
	rm -f dist/*
	rm -rf build/*

pypy3: clean
	$(PYPY3) setup.py sdist bdist_wheel
	$(PYPY3) setup.py install	

install: clean pkg
	$(PY3)  setup.py install --user

pkg: clean
	$(PY3) setup.py sdist bdist_wheel

uninstall: clean
	$(PIP3) uninstall scte35
	
upload: clean pkg	
	twine upload dist/*

upgrade:
	$(PIP3) install --upgrade scte35
	
cli:
	sed -i s/$(PYPY3)/$(PY3)/ scte35
	install scte35 /usr/local/bin
	
pypy3-cli:
	sed -i s/$(PY3)/$(PYPY3)/ scte35
	install scte35 /usr/local/bin


