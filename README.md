## Currencies
![trends](docs/trend.jpg)

---
### Day1: bootstrapping django, docker-composing environment.
---
```
# install development dependencies and obtain the shell with python venv. 
# see https://github.com/pypa/pipenv

[.] $ pipenv install --dev && pipenv shell

# run development environment

[.] $ docker compose up --build -d --remove-orphans

# create superuser inside container

[.] $ docker compose exec web bash
[container] $ ./manage createsuperuser
```
---
### Day2: setting jwt-auth and test-suite.
---
```
```