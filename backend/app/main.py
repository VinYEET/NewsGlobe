from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.news import router as news_router

app = FastAPI(title="Globe News API")

# Enable CORS so your front-end can call this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # restrict in prod
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# mount the /news router
app.include_router(news_router, prefix="/news", tags=["news"])
