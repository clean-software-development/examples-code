#!/usr/bin/env python

import json

import typer
from typer.colors import YELLOW, RED, GREEN

from project.models import User
from project.service import ProjectService

app = typer.Typer()


@app.command(name="create-tables")
def create_table():
    """Create all Dynamodb tables"""
    service = ProjectService()

    try:
        service.create_table()
    except Exception as err:
        print_message(str(err), color=RED)
    else:
        print_message("all tables have been created.", color=GREEN)


@app.command(name="add-user")
def add_user(username: str = None, user_id: str | None = None):
    """Add user to database"""
    service = ProjectService()
    try:
        user_id = service.add_user(user=User(username=username, user_id=user_id))
    except Exception as err:
        print_message(str(err), color=RED)
    else:
        print_message(f"user [{username}] created.", color=GREEN)


@app.command(name="get-user")
def get_user(user_id: str = None):
    """Display user from database"""
    service = ProjectService()
    try:
        user = service.get_user_by_id(user_id=user_id)
    except Exception as err:
        print_message(str(err), color=RED)
    else:
        print_message(json.dumps(user.model_dump(), indent=4), color=GREEN)


def print_message(message: str, color=YELLOW):
    message = typer.style(
        text=message,
        fg=color,
        bold=True
    )
    typer.echo(message=message)

if __name__ == "__main__":
    app()