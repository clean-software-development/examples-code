# Démonstration des tests unitaires AWS avec moto

## Installation

```shell
curl -sSL https://install.python-poetry.org | python3.10 -
git clone https://github.com/clean-software-development/examples-code
cd examples-code/tests-unitaires-aws-moto
poetry install
```

## Utilisation en ligne de commande

```shell
poetry run project-demo --help


# Créez les tables Dynamodb
poetry run project-demo create-tables


# Ajoutez un user
poetry run project-demo add-user --username myname --user-id 123abc
```

## Exécution des tests

```shell
poetry run pytest tests
```