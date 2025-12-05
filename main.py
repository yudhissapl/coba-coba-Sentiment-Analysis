from fastapi import FastAPI

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# Import models supaya tabel terdaftar di metadata
from modules.items.users import models as user_models
from modules.items.products import models as product_models
from modules.items.feedback import models as feedback_models

# Import router
from modules.items.users.routes import router as users_router
from modules.items.products.routes import router as products_router
from modules.items.feedback.routes import router as feedback_router
from modules.items.feedback.analytics import router as analytics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Project 2 - Sentiment Analysis API",
    description="CRUD User, Produk, Feedback + Analisis Sentimen",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(products_router)
app.include_router(feedback_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "Project 2 - Sentiment Analysis API is running"}