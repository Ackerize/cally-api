from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    try:
        supabase = get_db()
        response = supabase.table('users').insert({
            "email": user.email,
            "full_name": user.full_name,
            "auth_provider": user.auth_provider
        }).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Error creating user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    try:
        supabase = get_db()
        response = supabase.table('users').select("*").eq('id', str(user_id)).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))