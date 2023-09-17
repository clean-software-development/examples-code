from typing import Any
import logging

from project.domain.repository import RepositoryInterface, IdentityType

logger = logging.getLogger(__name__)


class RepositoryMemory(RepositoryInterface):

    def __init__(self, users: dict[IdentityType, Any] | None = None, posts: dict[IdentityType, Any] | None = None) -> None:
        self._users = users or {}
        self._posts = posts or {}

    def add_user(self, username: str, email: str) -> None:
        self._users[username] = {
            "username": username,
            "email": email
        }
    
    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        return self._users.get(username)

    def get_users(self, query_filter: dict[str, Any] | None = None) -> list[dict[str, Any] | None]:
        if query_filter:
            logger.warning("query_filter is not implemented for this repository")
        return self._users.values()