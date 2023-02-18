import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

import onboarding.app.auth.controllers as auth
import onboarding.app.healthcheck.controllers as healthcheck
import onboarding.app.news.controllers as news
import onboarding.app.profile.controllers as profile
import onboarding.app.tasks.controllers as tasks
import onboarding.app.library.controllers as library
import onboarding.exceptions as exceptions

from onboarding.config import settings
from onboarding.protocol import Response

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(healthcheck.router, tags=["healthcheck"])
app.include_router(auth.router, tags=["customers"], prefix="/api")
app.include_router(news.router, tags=["news"], prefix="/api")
app.include_router(profile.router, tags=["profile"], prefix="/api")
app.include_router(tasks.router, tags=["tasks"], prefix="/api")
app.include_router(library.router, tags=["library"], prefix="/api")


@app.exception_handler(Exception)
async def uvicorn_base_exception_handler(request: Request, exc: Exception):
    error = exceptions.ServerError(debug=str(exc))

    return ORJSONResponse(
        Response(
            code=error.status_code,
            payload=error.to_json(),
        ).dict()
    )


@app.exception_handler(exceptions.ApiException)
async def unicorn_api_exception_handler(request: Request, exc: exceptions.ApiException):
    return ORJSONResponse(
        Response(
            code=exc.status_code,
            payload=exc.to_json(),
        ).dict()
    )


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
