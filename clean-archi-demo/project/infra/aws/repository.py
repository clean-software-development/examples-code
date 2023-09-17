from typing import Any
import os
import logging
from uuid import uuid4

from boto3.session import Session
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table
from mypy_boto3_dynamodb.client import DynamoDBClient

from project.domain.entities import User
from project.domain.repository import RepositoryInterface, IdentityType
from project.domain.exceptions import UnknowError

logger = logging.getLogger(__name__)


class UserDynamodb(User):
    pass


class RepositoryDynamoDB(RepositoryInterface):

    def __init__(self, session: Session | None = None) -> None:
        
        self._session: Session = session or Session()
        self._dynamodb_client: DynamoDBClient = self._session.client("dynamodb")
        self._dynamodb_resource: DynamoDBServiceResource = self._session.resource("dynamodb")
                
        self._is_create_table: bool = os.getenv("PROJECT_IS_CREATE_TABLE") in ["true", "True", "1"]
        self._user_table_name: str = os.getenv("PROJECT_AWS_USER_TABLE_NAME") or "project-users"

        self._user_table: Table | None = None
        
        if self._is_create_table:
            self._create_table()

    def _create_table(self):
        logger.info("create dynamodb tables...")

        user_table = dict(
            TableName=self._user_table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        try:
            logger.info(f"create dynamodb table: {self._user_table_name}")
            self._dynamodb_client.create_table(**user_table)
            self._user_table = self._dynamodb_resource.Table(self._user_table_name)
            self._user_table.wait_until_exists()

            """
            client.update_time_to_live(
                TableName=self._user_table_name,
                TimeToLiveSpecification={"Enabled": True, "AttributeName": "ttl"},
            )
            """
        except Exception as err:
            logger.exception(str(err))
            raise UnknowError(str(err))          

    def add_user(self, username: str, email: str) -> None:
        try:
            user = UserDynamodb(username=username, email=email)
            self._user_table.put_item(Item=user.model_dump())
        except Exception as err:
            logger.exception(str(err))
            raise UnknowError(str(err))            
    
    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        try:
            response = self._user_table.get_item(Key={
                "username": username
            })
            return response.get("Item")
        except Exception as err:
            logger.exception(str(err))
            raise UnknowError(str(err))            

    def get_users(self, query_filter: dict[str, Any] | None = None) -> list[dict[str, Any] | None]:
        if query_filter:
            logger.warning("query_filter is not implemented for this repository")

        try:
            # TODO: pagination
            response = self._user_table.scan()
            return response.get("Items")
        except Exception as err:
            logger.exception(str(err))
            raise UnknowError(str(err))            
