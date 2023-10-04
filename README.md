## Currencies
![trends](docs/trend.jpg)

---
### [03.10.23] Day1: bootstrapping django, docker-composing environment.
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
### [04.10.23] Day2: setting jwt-auth up.
---
- [x] email-password jwt-based auth backend
---
### [05.10.23] Day3: firing celery up, implementing registration with email verification.
---
- [ ] celery
- [ ] registration
---
### [06.10.23] Day4: bootstrapping models, routing and test-suite.
---
- [ ] models
- [ ] routing
- [ ] tests
---
### [10.10.23] Day5: self-review.