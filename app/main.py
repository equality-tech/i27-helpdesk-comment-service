import os

# ✅ Optional local-only .env loading (won't break container)
try:
    from dotenv import load_dotenv
    env_file = os.getenv("ENV_FILE", "")
    if env_file:
        load_dotenv(env_file)
    else:
        # if you want local default
        load_dotenv(".env.local")
except Exception:
    pass
from fastapi import FastAPI
from sqlalchemy import text

# DB
from app.db.database import engine

# Models (important: registers metadata)
from app.models.comment import Comment

# Routes
from app.routes.comment_routes import router as comment_router

app = FastAPI(title="Comment Service")

# -----------------------------
# Startup DB connectivity check
# -----------------------------
@app.on_event("startup")
def startup_db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed:", e)
        raise e


# -----------------------------
# Health Endpoints
# -----------------------------
@app.get("/healthz")
def health():
    return {"status": "UP"}


@app.get("/readyz")
def ready():
    return {"status": "READY"}


# -----------------------------
# API Routes
# -----------------------------
app.include_router(comment_router)