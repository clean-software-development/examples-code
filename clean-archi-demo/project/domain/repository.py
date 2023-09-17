from abc import ABC, abstractmethod
from typing import Any, TypeVar
from uuid import UUID

IdentityType = TypeVar("IdentityType", str, int, UUID)


class RepositoryInterface(ABC):

    @abstractmethod
    def add_user(self, username: str, email: str) -> None:
        """Création d'un nouvel utilisateur.

        Args:
            username (str): Identifiant de l'utilisateur.

        Returns:
            None: Aucun retour

        Raises:
            ConflictError: Si l'utilisateur existe déjà        
        
        """
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> dict[str, Any]:
        """Recherche d'un utilisateur d'après son usernalme.

        Args:
            username (str): Identifiant de l'utilisateur.

        Returns:
            dict: Informations sur l'utilisateur

            {
                "username": "xxx",
                "email": "yyy@domain.net"
            }

        Raises:
            NotFoundError: Si l'utilisateur n'existe pas
        
        """

    @abstractmethod
    def get_users(self, query_filter: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Retourne la liste de tous les utilisateur
        
        Args:
            query_filter (dict): Filtre optionnel

        Returns:
            list(dict): Informations sur chaque utilisateur

            [
                {
                    "username": "xxx",
                    "email": "yyy@domain.net"
                }
            ]
        
        """
