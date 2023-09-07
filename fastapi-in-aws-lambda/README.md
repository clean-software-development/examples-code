# FastAPI dans une Lambda AWS

> **Requis: Python 3.10 avec pip**

Si vous ne disposez pas de Python 3.10 et vous souhaitez utiliser Terraform pour déployer, changer la version de python dans main.tf (maximum 3.10)

## Installation

```shell
python3.10 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel setuptools
pip install -r requirements-dev.txt
```

## Usage local

```shell
uvicorn app:app --reload
# Ouvrez l'url http://127.0.0.1:8000/docs
```

## Testabilité locale

```shell
pytest test_app.py
```

## Déploiement sur AWS

> **Requis: Compte AWS correctement configuré dans ~/.aws ou avec des variables d'environnement**

```shell
terraform init
terraform validate
terraform plan
terraform apply
```
