fmt:
	cd src && autoflake --in-place --remove-all-unused-imports --recursive .
	cd src && isort .
	cd src && black .

up:
	docker compose up --build --remove-orphans -d

down:
	docker compose down

psql:
	docker compose exec -ti postgres bash -c "su -c psql postgres"

superuser:
	docker compose exec -ti web bash -c "./manage.py createsuperuser"