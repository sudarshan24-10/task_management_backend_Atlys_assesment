from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from logger import Logger
from database.db_initialize import DatabaseInitializer
from user.routes.user_route import user_router
from task.routes.task_route import task_router
import uvicorn

logger = Logger().get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    db_initializer = DatabaseInitializer()
    dbs = await db_initializer.db_init()
    app.state.db = dbs["mongo"]
    logger.info("Database initialized successfully!")
    yield  
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Task Management API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,  
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check
    @app.get("/health", tags=["Health"])
    async def health_check():
        logger.info("Health check endpoint called.")
        return {"status": "ok"}

    # Routes
    app.include_router(user_router, prefix="/user")
    app.include_router(task_router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=True)
