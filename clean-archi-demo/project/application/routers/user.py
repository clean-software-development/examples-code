import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status as http_status

from project.domain.entities import User, IdentityType
from project.domain.exceptions import ProjectException
from project.infra.project_infra import ProjectInfra
from project.application.models import AddUserResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    path="",
    response_model=AddUserResponse
)
async def add_user(user: User) -> JSONResponse:
    try:
        return AddUserResponse(id=ProjectInfra.service.add_user(user=user))
    except ProjectException as err:
        logger.error(str(err))
        return JSONResponse(
            content=err.message,
            status_code=err.status_code
        )
    except Exception as err:
        logger.exception(str(err))
        return JSONResponse(
            content=str(err),
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR
        )