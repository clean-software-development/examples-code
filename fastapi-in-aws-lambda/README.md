# FastAPI dans une Lambda AWS

## Installation

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel setuptools
pip install -r requirements.txt
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

TODO...