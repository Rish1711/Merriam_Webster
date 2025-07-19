# Variables
PYTHON = /usr/bin/python3
APP_DIR = app
LOG_DIR = logs
TEST_FILE = $(APP_DIR)/merriam_webster_test.py
LOG_FILE = $(LOG_DIR)/merriam_webster.log
REQUIREMENTS = requirements.txt

# Default target
.PHONY: all
all: test

# Install dependencies
.PHONY: install
install:
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

# Run tests
.PHONY: test
test:
	PYTHONPATH=$(APP_DIR) $(PYTHON) -m pytest $(TEST_FILE) -v

# Clean logs
.PHONY: clean
clean:
	rm -f $(LOG_FILE)
	echo "Logs cleaned."

# Run the application with example word
.PHONY: run
run:
	$(PYTHON) $(APP_DIR)/merriam_webster.py $(word)

# Lint the code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 $(APP_DIR)

# Help message
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install   - Install dependencies from requirements.txt"
	@echo "  test      - Run tests using pytest"
	@echo "  clean     - Clean up log files"
	@echo "  run       - Run the application with a sample word"
	@echo "  lint      - Lint the code using flake8"
	@echo "  help      - Show this help message"
