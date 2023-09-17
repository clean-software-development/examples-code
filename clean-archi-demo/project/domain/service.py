from typing import Any
import logging

from project.domain.entities import User
from project.domain.repository import RepositoryInterface
from project.domain.exceptions import ConflictError, NotFoundError

logger = logging.getLogger(__name__)


class Service:
    """Tout les Usecases de ce projet avec les règles métiers"""

    def __init__(self, repository: RepositoryInterface) -> None:
        self.repository: RepositoryInterface = repository

    def add_user(self, user: User) -> None:
        logger.info(f"add user [{user.username}]")
        # TODO: add control if + in email
        # TODO: add control if email pro
        # TODO: add control if in blacklist
        # TODO: déclenche opérations en cascade ?
        existing_user = self.repository.get_user_by_username(username=user.username)

        if existing_user:
            msg = f"this user [{user.username}] already exists"
            logger.error(msg)
            raise ConflictError(msg)

        return self.repository.add_user(**user.model_dump())

    def get_user_by_username(self, username: str) -> User:
        user = self.repository.get_user_by_username(username=username)

        if not user:
            msg = f"user [{username}] not found"
            logger.error(msg)
            raise NotFoundError(msg)

        return User(**user)

    def get_users(self, query_filter: dict[str, Any] | None = None) -> list[User]:
        return [
            User(**item)
            for item in self.repository.get_users(query_filter=query_filter)
        ]
