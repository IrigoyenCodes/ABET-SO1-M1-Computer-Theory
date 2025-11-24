# Makefile for Lexical and Semantic Analyzer

.PHONY: help test clean install run examples lint format

# Default target
help:
	@echo "Lexical and Semantic Analyzer - Build System"
	@echo ""
	@echo "Available commands:"
	@echo "  make test     - Run the test suite"
	@echo "  make run      - Run the analyzer with default example"
	@echo "  make examples - Run analyzer on example files"
	@echo "  make install  - Install dependencies"
	@echo "  make clean    - Clean temporary files"
	@echo "  make lint     - Run code linting"
	@echo "  make format   - Format code with black"
	@echo "  make help     - Show this help message"

# Run tests
test:
	@echo "Running test suite..."
	python tests.py

# Run analyzer with default example
run:
	@echo "Running analyzer with default example..."
	python main.py

# Run analyzer on example files
examples:
	@echo "Running analyzer on valid program..."
	python main.py examples/valid_program.c
	@echo ""
	@echo "Running analyzer on error program..."
	python main.py examples/error_program.c
	@echo ""
	@echo "Running analyzer on control flow example..."
	python main.py examples/control_flow.c

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/

# Run linting (if pylint is installed)
lint:
	@echo "Running linting..."
	@if command -v pylint >/dev/null 2>&1; then \
		pylint main.py; \
	else \
		echo "pylint not installed. Install with: pip install pylint"; \
	fi

# Format code (if black is installed)
format:
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black *.py; \
	else \
		echo "black not installed. Install with: pip install black"; \
	fi

# Check Python version
check-version:
	@python -c "import sys; print(f'Python version: {sys.version}'); sys.exit(0 if sys.version_info >= (3, 9) else 1)"

# Full CI pipeline
ci: check-version test lint
	@echo "CI pipeline completed successfully!"
