from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import(
    user as user_routes,
    gangsheets as gang_sheets,
    cleanup as clean_up,
)
from database.db import engine, Base

app = FastAPI()
# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow the React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(user_routes.router)
app.include_router(gang_sheets.router)
app.include_router(clean_up.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)