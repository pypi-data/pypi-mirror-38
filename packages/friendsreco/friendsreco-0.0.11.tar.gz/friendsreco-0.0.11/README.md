[![Build Status](https://circleci.com/gh/dutradda/friendsreco.svg?style=svg)](https://circleci.com/gh/dutradda/friendsreco)
[![Coverage Status](https://coveralls.io/repos/github/dutradda/friendsreco/badge.svg?branch=master)](https://coveralls.io/github/dutradda/friendsreco?branch=master)
[![PyPi Last Version](https://img.shields.io/pypi/v/friendsreco.svg)](https://pypi.python.org/pypi/friendsreco)
[![PyPi Develop Status](https://img.shields.io/pypi/status/friendsreco.svg)](https://pypi.python.org/pypi/friendsreco)
[![Python Versions](https://img.shields.io/pypi/pyversions/friendsreco.svg)](https://pypi.python.org/pypi/friendsreco)
[![License](https://img.shields.io/pypi/l/friendsreco.svg)](https://github.com/dutradda/friendsreco/blob/master/LICENSE)

# friendsreco
A simple HTTP friends recommendations service


Running locally:

- Install minikube as in [doc](https://kubernetes.io/docs/tasks/tools/install-minikube/)
- Install helm package manager as in [doc](https://docs.helm.sh/using_helm/)
- Install friendsreco helm package: `make deploy`
- Proxy ports: `kubectl port-forward deploy/friendsreco 7474:7474 7687:7687 6000:6000 8080:8080`
- Activate debug messages, if desired: `make debug-deploy`


These steps can be used to deploy the application on cloud too.


Running tests:
 - `pip install tox && tox`


Get friendships for the given people:

- `curl -i localhost:8080/friendships?who=Arthur,Mari`


Get all friendships:

- `curl -i localhost:8080/friendships`


Create recommendations:

- `curl -i -X POST localhost:8080/recommendations`


Get recommendations for a given person:

- `curl -i localhost:8080/recommendations/Arthur`


Get all recommendations:

- `curl -i localhost:8080/recommendations`
