SHELL := /bin/bash
BUILD_DIR := ./build
TARGET_DIR := ./target
VIRTUALENV_DIR := $(BUILD_DIR)/venv
PYTHON := $(VIRTUALENV_DIR)/bin/python
PIP := $(VIRTUALENV_DIR)/bin/pip
SOURCES := $(shell echo src/*.py)
TARGETS := $(patsubst src/%.py,target/%.json,$(SOURCES))

all: setup $(TARGETS)

clean:
	rm -f $(TARGETS)
	rm -rf ${BUILD_DIR}
	find . -name "*.py[co]" -delete

target/%.json: src/%.py
	${PYTHON} $< > $@

${TARGET_DIR}:
	mkdir -p ${TARGET_DIR}

setup: venv ${TARGET_DIR}
	${PIP} install -Ur requirements.txt

venv:
	test -d ${VIRTUALENV_DIR}/bin || virtualenv ${VIRTUALENV_DIR}

deploy:
	${PYTHON} deploy.py
