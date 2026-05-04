from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import time
from app.core.config import settings
from app.core.database import engine, Base
from app.modules.users import models as user_models
from app.modules.events import models as event_models
from app.modules.registrations import models as registration_models
from app.modules.checklist import models as checklist_models
from app.modules.users.router import router as users_router
from app.modules.events.router import router as events_router
from app.modules.registrations.router import router as registrations_router
from app.modules.checklist.router import router as checklist_router


def wait_for_db(max_retries=10, delay=2):
    """Wait for database to be ready"""
    engine = create_engine(settings.DATABASE_URL)
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            return
        except OperationalError as e:
            print(
                f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}"
            )
            time.sleep(delay)
    raise Exception("Could not connect to database after multiple retries")


wait_for_db()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Event Management API",
    description="API for organizing events and meetings",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Event Management API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
