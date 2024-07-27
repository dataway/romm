import re
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import alembic.config
import endpoints.sockets.scan  # noqa
import uvicorn
from config import (
    DEV_HOST,
    DEV_PORT,
    DISABLE_CSRF_PROTECTION,
    IS_PYTEST_RUN,
    ROMM_AUTH_SECRET_KEY,
    SCAN_TIMEOUT,
)
from endpoints import (
    auth,
    collections,
    config,
    feeds,
    firmware,
    heartbeat,
    platform,
    raw,
    rom,
    saves,
    screenshots,
    search,
    states,
    stats,
    tasks,
    user,
)
from endpoints.sockets.scan import scan_platforms
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from handler.auth.base_handler import ALGORITHM
from handler.auth.hybrid_auth import HybridAuthBackend
from handler.auth.middleware import CustomCSRFMiddleware, SessionMiddleware
from handler.redis_handler import high_prio_queue
from handler.scan_handler import ScanType
from handler.socket_handler import socket_handler
from starlette.middleware.authentication import AuthenticationMiddleware
from utils import get_version
from utils.context import ctx_httpx_client, initialize_context, set_context_middleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with initialize_context():
        app.state.httpx_client = ctx_httpx_client.get()
        yield


app = FastAPI(title="RomM API", version=get_version(), lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not IS_PYTEST_RUN and not DISABLE_CSRF_PROTECTION:
    # CSRF protection (except endpoints listed in exempt_urls)
    app.add_middleware(
        CustomCSRFMiddleware,
        secret=ROMM_AUTH_SECRET_KEY,
        exempt_urls=[re.compile(r"^/token.*"), re.compile(r"^/ws")],
    )

# Enable GZip compression for responses
app.add_middleware(GZipMiddleware, minimum_size=1024)

# Handles both basic and oauth authentication
app.add_middleware(
    AuthenticationMiddleware,
    backend=HybridAuthBackend(),
)

# Enables support for sessions on requests
app.add_middleware(
    SessionMiddleware,
    secret_key=ROMM_AUTH_SECRET_KEY,
    session_cookie="romm_session",
    same_site="strict",
    https_only=False,
    jwt_alg=ALGORITHM,
)

# Sets context vars in request-response cycle
app.middleware("http")(set_context_middleware)

app.include_router(heartbeat.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(platform.router)
app.include_router(rom.router)
app.include_router(search.router)
app.include_router(saves.router)
app.include_router(states.router)
app.include_router(tasks.router)
app.include_router(feeds.router)
app.include_router(config.router)
app.include_router(stats.router)
app.include_router(raw.router)
app.include_router(screenshots.router)
app.include_router(firmware.router)
app.include_router(collections.router)

app.mount("/ws", socket_handler.socket_app)


if __name__ == "__main__":
    # Run migrations
    alembic.config.main(argv=["upgrade", "head"])

    # Run a no-scan in the background on startup
    high_prio_queue.enqueue(
        scan_platforms, [], ScanType.NO_SCAN, [], [], job_timeout=SCAN_TIMEOUT
    )

    # Run application
    uvicorn.run("main:app", host=DEV_HOST, port=DEV_PORT, reload=True)
