import logging
from uuid import uuid4
import os

from boto3.session import Session
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table
from mypy_boto3_dynamodb.client import DynamoDBClient
from project.models import User

logger = logging.getLogger(__name__)


class ProjectService:

    def __init__(self) -> None:
        self._session: Session = Session()
        self._dynamodb_client: DynamoDBClient = self._session.client("dynamodb")
        self._dynamodb_resource: DynamoDBServiceResource = self._session.resource("dynamodb")
                
        self.__user_table: Table | None = None
        self._user_table_name: str | None = os.getenv("PROJECT_USER_TABLE_NAME") or "project-users"

    def create_table(self):
        logger.info("create dynamodb tables...")

        user_table = dict(
            TableName=self._user_table_name,
            AttributeDefinitions=[
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        try:
            logger.info(f"create dynamodb table: {self._user_table_name}")
            self._dynamodb_client.create_table(**user_table)
            self.__user_table = self._dynamodb_resource.Table(self._user_table_name)
            self.__user_table.wait_until_exists()
        except Exception as err:
            logger.exception(str(err))
            raise

    def get_user_table(self) -> Table:
        try:
            self.__user_table: Table = self._dynamodb_resource.Table(name=self._user_table_name)
            self.__user_table.load()
            return self.__user_table
        except self._dynamodb_resource.meta.client.exceptions.ResourceNotFoundException as err:
            logger.error(str(err))
            raise Exception(f"La table {self._user_table_name} n'existe pas.")
        except Exception as err:
            logger.exception(str(err))
            raise

    def add_user(self, user: User) -> str:
        try:
            if not user.user_id:
                user.user_id = str(uuid4())

            self.user_table.put_item(Item=user.model_dump())
            
            return user.user_id
        except Exception as err:
            logger.exception(str(err))
            raise 
    
    def get_user_by_id(self, user_id: str) -> User:
        try:
            response = self.user_table.get_item(Key={"user_id": user_id})
            if not response.get('Item'):
                raise Exception(f"User not found for id: {user_id}")
            return User(**response.get('Item'))
        except Exception as err:
            logger.exception(str(err))
            raise 
    
    user_table: Table = property(get_user_table)
