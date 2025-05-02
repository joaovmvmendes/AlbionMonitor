# Nome da imagem Docker
IMAGE_NAME = albion-monitor

# Caminho para os scripts de importação
PYTHON := python3
IMPORT_DIR := imports

# Comando para construir a imagem Docker
build:
	docker build -t $(IMAGE_NAME) .

# Comando para rodar o container Docker com as variáveis de ambiente
run:
	docker run \
		-e ITEM_NAME="T8_SHOES_CLOTH_SET3@2" \
		-e CITIES="Caerleon,Bridgewatch,Thetford,Martlock,Fortsterling,Lymhurst,Brecilien" \
		-e TELEGRAM_TOKEN="7843081611:AAFvQtLkRt3i28J8DM3Pruq7A0h30bKbRII" \
		-e TELEGRAM_CHAT_ID="6116794414" \
		-e agrupamento="city" \
		$(IMAGE_NAME)

# Comando para construir a imagem e rodar o container em sequência
run-local: build run

# --- COMANDOS PARA IMPORTAÇÃO DE DADOS ---

# Reset completo do banco
reset-db:
	@echo "🧨 Resetando banco de dados..."
	psql -U postgres -d albiondb -h localhost -f $(IMPORT_DIR)/create_items_schema.sql

# Importa todos os dados
import-all: import-base import-aux import-details import-localizations

import-aux:
	@echo "📦 Importando tabela auxiliar dos itens..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_aux_tables.py

import-base:
	@echo "📦 Importando itens base..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_items_base.py

import-details:
	@echo "⚙️  Importando detalhes dos itens..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_items_details.py

import-localizations:
	@echo "🌍 Importando localizações..."
	PYTHONPATH=. $(PYTHON) $(IMPORT_DIR)/import_localizations.py

remount-db: reset-db import-all

.PHONY: build run run-local reset-db import-all import-base import-details import-localizations