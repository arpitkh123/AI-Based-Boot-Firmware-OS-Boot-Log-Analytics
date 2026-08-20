from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from api.routes import router
# from database.init_db import init_db

from backend.api.routes import router
from backend.database.init_db import init_db

# Initialize database tables
init_db()

app = FastAPI(
    title="AI Boot Log Analytics API"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
def root():

    return {
        "message": "Backend Running"
    }