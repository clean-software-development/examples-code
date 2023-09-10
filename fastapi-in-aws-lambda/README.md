# FastAPI dans une Lambda AWS

## Pré-requis

- Python 3.10 avec virtuelenv et pip
- Docker (optionnel)
- Terraform (optionnel)

Si vous ne disposez pas de Python 3.10 et que vous souhaitez utiliser Terraform pour déployer, changez la version de python dans main.tf (maximum 3.10 pour les lambdas)

## Installation

```shell
curl -sSL https://install.python-poetry.org | python3.10 -
# Sur Mac OS si vous avez des problème de certificat avec curl:
# sudo port install curl-ca-bundle

git clone https://github.com/clean-software-development/examples-code
cd examples-code/fastapi-in-aws-lambda/project
poetry install
```

## Usage local

```shell
poetry run uvicorn fastapi_in_aws_lambda.app:app --reload
# Ouvrez l'url http://127.0.0.1:8000/docs
```

## Testabilité locale

```shell
poetry run pytest test_app.py
```

## Déploiement sur AWS

> **Requis: Compte AWS correctement configuré dans ~/.aws ou avec des variables d'environnement**

```shell
cd terraform
terraform init
terraform plan

# Si vous êtes sous Mac OS déclarez la variable:
# export DOCKER_DEFAULT_PLATFORM=linux/amd64

terraform apply
```

> Après un déploiement réussi, vous aurez l'url d'accès à l'api sur la console. Ouvrez l'url pour découvrir le swagger.

```shell
apigateway_url = "https://XXXX.execute-api.eu-west-3.amazonaws.com"
```

> Ouvrez l'url https://XXXX.execute-api.eu-west-3.amazonaws.com/docs

![Swagger](fastapi-in-aws-lambda/img/swagger.png)