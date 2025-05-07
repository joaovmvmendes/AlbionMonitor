PYTHON := python3
IMAGE_NAME := albion-monitor

.PHONY: build run run-local test lint coverage clean help

# 🔧 Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# ▶️ Run the container with environment variables from .env
run:
	docker run --env-file .env $(IMAGE_NAME)

# 🔁 Build and run locally
run-local: build run

# 🧪 Run all unit tests
test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests

# 🧼 Check code formatting
lint:
	black . --check
	flake8

# 🧪 Generate test coverage report
coverage:
	@command -v coverage >/dev/null 2>&1 || { \
		echo >&2 "❌ coverage is not installed. Run: pip install coverage"; exit 1; }
	rm -rf htmlcov
	coverage run -m unittest discover -s tests
	coverage html
	@echo "✅ Coverage report generated at htmlcov/index.html"


# 🧹 Clean Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# 📚 Help message
help:
	@echo "Available Make targets:"
	@echo "  build       - Build Docker image"
	@echo "  run         - Run container with .env variables"
	@echo "  run-local   - Build and run locally"
	@echo "  test        - Run all unit tests"
	@echo "  lint        - Check code style (black + flake8)"
	@echo "  coverage    - Generate test coverage report"
	@echo "  clean       - Remove __pycache__ and .pyc files"