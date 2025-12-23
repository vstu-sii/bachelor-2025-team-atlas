import asyncio
import logging

from litestar import Litestar, get
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.exceptions import HTTPException
import uvicorn

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

@get("/")
async def root() -> str:
    return "root"

@get("/status/{status_code:int}")
async def return_status(
    status_code: int,
    seconds_sleep: int | None = None,
) -> dict:
    logger.info(f"Hello from Litestar! {status_code=}, {seconds_sleep=}")
    if seconds_sleep:
        await asyncio.sleep(seconds_sleep)
    if status_code and status_code != 200:
        logger.error("Shit happens")
        raise HTTPException(detail="an error occurred", status_code=status_code)
    return {"data": "Hello"}

prometheus_config = PrometheusConfig()

app = Litestar(
    route_handlers=[root, return_status, PrometheusController],
    middleware=[prometheus_config.middleware],
    openapi_config=OpenAPIConfig(
        title="Тестовый Бэкенд",
        description="Пример OpenAPI документации",
        version="0.0.1",
        render_plugins=[ScalarRenderPlugin()],
        path="/docs",
    ),
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False, workers=1)