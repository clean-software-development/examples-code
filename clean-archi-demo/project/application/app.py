from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from project.application.routers.user import router as user_router


def _add_routers(app: FastAPI):

    # @app.get(f"/", include_in_schema=False)
    # def redirect_doc():
    #     return RedirectResponse(url=app.url_path_for("doc-swagger"))

    app.include_router(
        user_router,
        prefix=f"/user",
        include_in_schema=True,
    )


def create_app() -> FastAPI:

    app = FastAPI(
        title="¨Project API",
        version="0.1.0",
        root_path_in_servers=False,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    _add_routers(app)
    
    return app
