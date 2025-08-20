# Nome do serviço no docker-compose
SERVICE=web

# Caminho do banco de dados
DB_PATH=./db.sqlite3

# Diretório onde os apps são criados
APPS_DIR=.

# Nome do container para referência rápida
define docker_run
	docker compose exec $(SERVICE) python manage.py
endef

# Criar novo app: make newapp name=nome_do_app
newapp:
	$(docker_run) startapp $(name) $(APPS_DIR)/$(name)

# Rodar as migrações
migrate:
	$(docker_run) makemigrations
	$(docker_run) migrate

# Apagar banco de dados e migrações
reset:
	rm -f $(DB_PATH)
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete
	$(docker_run) makemigrations
	$(docker_run) migrate

# Subir o projeto
up:
	docker compose up

# Parar containers
down:
	docker compose down

# Enviar branch repositorio publico: make push-public branch=nome_da_branch
push-public:
	git push public $(branch)


# Criar virtualenv
create-venv:
	python3 -m venv venv

# Ativar virtualenv
activate-venv:
	. venv/bin/activate

# Rodar o servidor com virtualenv ativado
run:
	. venv/bin/activate 
	pip3 install -r requirements.txt
	python3 manage.py runserver