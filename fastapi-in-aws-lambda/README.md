# FastAPI dans une Lambda AWS

## Pré-requis

- Python 3.10 avec virtuelenv et pip
- Docker

Si vous ne disposez pas de Python 3.10 et que vous souhaitez utiliser Terraform pour déployer, changer la version de python dans main.tf (maximum 3.10 pour les lambdas)

## Installation

```shell
curl -sSL https://install.python-poetry.org | python3.10 -
# Sur Mac OS si vous avez des problème de certificat avec curl:
# sudo port install curl-ca-bundle

cd fastapi-in-aws-lambda
python3.10 -m venv .venv
source .venv/bin/activate
poetry install
```

## Usage local

```shell
poetry run uvicorn app:app --reload
# Ouvrez l'url http://127.0.0.1:8000/docs
```

## Testabilité locale

```shell
pytest test_app.py
```

## Déploiement sur AWS

> **Requis: Compte AWS correctement configuré dans ~/.aws ou avec des variables d'environnement**

```shell
cd terraform

terraform init

terraform validate

terraform plan

# Si vous êtes sous Mac OS déclarer la variable:
# export DOCKER_DEFAULT_PLATFORM=linux/amd64

terraform apply
```

> Après un déploiement réussi, vous aurez l'url d'accès à l'api sur la console: ex:

```shell
apigateway_url = "https://XXXX.execute-api.eu-west-3.amazonaws.com"
lambda_function_invoke_arn = "arn:aws:apigateway:eu-west-3:lambda:path/2015-03-31/functions/arn:aws:lambda:eu-west-3:316694718945:function:fastapi-in-aws-lambda-function/invocations"
lambda_function_url = "https://mx6wr4cl7juw3x2po6hidtbysu0csevb.lambda-url.eu-west-3.on.aws/"
```

> Ouvrez l'url https://XXXX.execute-api.eu-west-3.amazonaws.com/docs