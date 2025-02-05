from fastapi import FastAPI, HTTPException
from app.core.config import Settings
from app.core.database import get_db
from app.api.v1 import users, images

settings = Settings()
app = FastAPI(title=settings.app_name)

# Include routers
app.include_router(users.router, prefix="/api/v1")
app.include_router(images.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}"}

@app.get("/test-db")
async def test_db_connection():
    try:
        supabase = get_db()
        response = supabase.rpc('check_connection').execute()
        
        return {
            "status": "success",
            "message": "Database connection successful",
            "data": response.data
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )