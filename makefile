# === AlbionMonitor Makefile ===
# Manage Docker containers, database schema, data import routines, and cleanup

# === Container Management ===

start:
	@echo "🚀 Building and starting AlbionMonitor containers..."
	docker-compose up -d --build
	@echo "✅ All services are up and running."

stop:
	@echo "🛑 Stopping all containers..."
	docker-compose down

logs:
	docker-compose logs -f albionmonitor

rebuild:
	@echo "♻️ Rebuilding all containers from scratch..."
	docker-compose down -v --remove-orphans
	docker-compose up -d --build

shell:
	docker exec -it albion-monitor /bin/bash

shell-db:
	docker exec -it albion-postgres psql -U postgres -d albiondb

# === Environment Cleanup ===

clean:
	@echo "🧹 Cleaning Docker containers, images, volumes, and environment..."
	docker-compose down -v --remove-orphans
	docker system prune -af --volumes
	@echo "🧼 Removing virtual environment and __pycache__..."
	rm -rf .venv
	find . -type d -name '__pycache__' -exec rm -rf {} +
	@echo "✅ Full cleanup complete. Ready for a fresh start."

reset-db:
	@echo "🗑️ Resetting PostgreSQL database volume..."
	docker-compose stop postgres
	docker volume rm albion-postgres
	docker-compose up -d postgres
	@echo "✅ Database volume recreated. You can now re-import data or reinitialize."

# === Schema Initialization ===

init-db:
	@echo "📦 Creating normalized tables from Albion schema..."
	cat imports/schemas/item_localizations_schema.sql | docker exec -i albion-postgres psql -U postgres -d albiondb
	@echo "✅ Schema successfully initialized."

# === Imports (Core and Specialized) ===

import-localization:
	@echo "📥 Importing all base item data..."
	docker-compose --env-file .env run --rm -e PYTHONPATH=/AlbionMonitor albionmonitor python imports/loaders/handlers/import_localizations.py
	@echo "✅ All item data imported."

# === Full Reset Routine ===

reset:
	@echo "♻️ Performing full reset: cleaning, rebuilding and importing..."
	@$(MAKE) clean
	sleep 10
	@$(MAKE) start
	sleep 10
	@$(MAKE) init-db
	sleep 10
	@$(MAKE) import-localization
	@echo "✅ Full reset completed."

# === Help Message ===

help:
	@echo "📘 AlbionMonitor Makefile Commands:"
	@echo ""
	@echo " 🐳 Containers:"
	@echo "   make start        → Build and start containers"
	@echo "   make stop         → Stop all containers"
	@echo "   make logs         → Tail logs from albionmonitor"
	@echo "   make rebuild      → Rebuild all containers"
	@echo "   make shell        → Access container shell"
	@echo "   make shell-db     → Open PostgreSQL interactive shell"
	@echo ""
	@echo " 💾 Database:"
	@echo "   make init-db      → Initialize schema using SQL file"
	@echo "   make reset-db     → Drop and recreate DB volume"
	@echo ""
	@echo " 📦 Import:"
	@echo "   make import-all   → Import all item-related data"
	@echo "   make reset        → Clean environment and fully reimport"
	@echo ""
	@echo " 🧼 Cleanup:"
	@echo "   make clean        → Remove containers, images, volumes, .venv, and __pycache__"