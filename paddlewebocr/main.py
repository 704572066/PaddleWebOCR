import sys
import os
import click
import logging
from loguru import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from paddlewebocr.pkg.config import settings
from paddlewebocr.pkg.log import InterceptHandler, format_record
from paddlewebocr.route.api import api_router


def make_app():
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG,
    )

    logging.getLogger().handlers = [InterceptHandler()]

    logger.configure(
        handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}]
    )
    logger.add(settings.LOG_FILE, encoding='utf-8', rotation="9:46")

    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.") or name.startswith("paddle.")
    )
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("paddle").handlers = [InterceptHandler()]
    logger.info("Starting {}", settings.PROJECT_NAME)
    return app


app = make_app()

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount("/", StaticFiles(directory=os.path.join(".", "webui", "dist"), html=True), name="static")


@click.command()
@click.option("--bind", default='0.0.0.0', help="service bind address")
@click.option("--port", default=8080, help="service port")
# @click.option("--debug", default=True, help="debug mode")
def main(bind, port):
    import uvicorn
    uvicorn.run(app, host=bind, port=port, workers=8)


if __name__ == "__main__":
    main()
