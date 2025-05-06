PYTHON := python3
IMAGE_NAME := albion-monitor
IMPORT_DIR := imports

.PHONY: build run run-local reset-db import-all import-base import-details import-localizations remount-db help

# Build Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container with environment variables
run:
	docker run \
		-e ITEM_NAME="T8_SHOES_CLOTH_SET3@2" \
		-e CITIES="Caerleon,Bridgewatch,Thetford,Martlock,Fortsterling,Lymhurst,Brecilien" \
		-e TELEGRAM_TOKEN="$(TELEGRAM_TOKEN)" \
		-e TELEGRAM_CHAT_ID="$(TELEGRAM_CHAT_ID)" \
		-e GROUPING="city" \
		$(IMAGE_NAME)

# Build and run container locally
run-local: build run

# Reset the database
reset-db:
	@echo "💣 Resetting database..."
	psql -U postgres -d albiondb -h localhost -f $(IMPORT_DIR)/create_items_schema.sql

# Import all item-related data
import-all: import-base import-aux import-details import-localizations

import-aux:
	@echo "📦 Importing auxiliary item tables..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_aux_tables.py

import-base:
	@echo "📦 Importing base item definitions..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_items_base.py

import-details:
	@echo "⚙️  Importing item detail data..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_items_details.py

import-localizations:
	@echo "🌍 Importing localization strings..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_localizations.py

# Reset and repopulate the database
remount-db: reset-db import-all

# Help message
help:
	@echo "Available Make targets:"
	@echo "  build              - Build Docker image"
	@echo "  run                - Run monitor in container"
	@echo "  run-local          - Build and run locally"
	@echo "  reset-db           - Drop and recreate DB schema"
	@echo "  import-all         - Import all item data"
	@echo "  remount-db         - Reset and import everything"

# Run all tests and generate clean coverage report
coverage:
	rm -rf htmlcov
	coverage run -m unittest discover -s tests
	coverage html
	@echo "✅ Coverage report generated at htmlcov/index.html"
