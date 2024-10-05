import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Settings
from src.services.data_transfer_testit.routers import router_migration

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_migration)

settings = Settings()

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.host_system,
        port=settings.port_system,
        log_level=settings.log_level,
        access_log=settings.access_log
        )
