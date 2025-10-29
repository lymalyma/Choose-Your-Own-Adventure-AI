from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings 
# Now import the routers into the main app... 
from routers import story, job

# --- FIX IS HERE ---
# Import the models just so create_tables() works,
# but give them a different name (or don't import them at all, see below).
import models.story
import models.job
# --- END FIX ---
from db.database import create_tables

create_tables()

app = FastAPI(
    title="Choose Your own Adventure Game API", 
    description="Api to generate cool stories", 
    version="0.1.0",
    docs_url="/docs", 
    redoc_url="/redoc" 

)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.ALLOWED_ORIGINS, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
    )

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(job.router, prefix=settings.API_PREFIX)


if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
