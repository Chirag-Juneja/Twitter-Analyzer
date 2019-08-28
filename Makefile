################################################################################
# Project		: Anton
# File			: Makefile
# Version		: v1.0
# Created By	: Chirag Juneja <chiragjuneja6@gmail.com>
# Description	: Makefile to automate tasks
################################################################################

ENVIRONMENT = venv

environment:
	virtualenv -p /usr/bin/python3 $(ENVIRONMENT)

install-dep:
	pip install -r dependencies

export-dep:
	pip freeze > dependencies

run:
	python anton/app.py 

test:
	@pytest tests | tee test-results.log

clean:
	py3clean .