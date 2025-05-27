from fastapi import FastAPI, status
from pydantic import BaseModel
from core.configs import settings
from api.v1.api import api_router
import uvicorn

app = FastAPI(title='UrbanFood - Microserviço de Produtos')
app.include_router(api_router, prefix=settings.API_V1_STR)

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""
    status: str = "OK"

@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


def main() -> None:
    """Entrypoint to invoke when this module is invoked on the remote server."""
    # See the official documentations on how "0.0.0.0" makes the service available on
    # the local network - https://www.uvicorn.org/settings/#socket-binding
    uvicorn.run("main:app", host="0.0.0.0", port=8003, log_level='info', reload=True)

if __name__ == "__main__":
    main()
