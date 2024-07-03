default: help

# --------------------------- MAKEFILE VARIABLES ---------------------------
FORMATTING_COLOR_YELLOW = \033[33m
FORMATTING_COLOR_BLUE= \033[36m
FORMATTING_END = \033[0m

#? ########################### MAKEFILE COMMANDS #########################


.PHONY: help
help: ## Show this help
	@printf -- "%s\n" \
	" " \
	"------ GuestReady Challenge TOOL------------------------------------------------------------- " \
	" " \
	"This makefile provides commands to manage the deployment of the Django service and the REST Api with postgres database. " \
	"Usage: make <command> [options] " \
	" " \
	"------------------------------------------------------------------------------------------ " \
	""
	@echo "${FORMATTING_COLOR_YELLOW}Commands:${FORMATTING_END}"
	@awk -F ':.*?## ' '/^[a-zA-Z0-9_-.]+:.*?##/ {printf "  ${FORMATTING_COLOR_BLUE}%-12s -> ${FORMATTING_END} %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo


up: ## Launch the docker compose
	@docker compose -f docker-compose.yml up --build --detach

down: ## Stops all containers 
	@docker compose -f docker-compose.yml down --remove-orphans 

remove: ## Remove all containers and volumes 
	@docker compose -f docker-compose.yml down --volumes --remove-orphans

tests: ## Run mypy, pytest and tox in the repo (development)
	@tox 

dev.api: ## Run the API directly in the terminal (development)
	@cd services/restapi; python3 api