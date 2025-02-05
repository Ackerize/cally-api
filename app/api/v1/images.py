from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import UUID
from app.schemas.image import ImageCreate, ImageResponse
from app.core.database import get_db

router = APIRouter(prefix="/images", tags=["images"])

@router.post("/", response_model=ImageResponse)
async def upload_image(image: ImageCreate):
    try:
        supabase = get_db()
        response = supabase.table('images').insert({
            "user_id": str(image.user_id),
            "original_image_url": str(image.original_image_url),
            "processed_image_url": str(image.processed_image_url) if image.processed_image_url else None
        }).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Error uploading image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=List[ImageResponse])
async def get_user_images(user_id: UUID):
    try:
        supabase = get_db()
        response = supabase.table('images').select("*").eq('user_id', str(user_id)).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{image_id}/process", response_model=ImageResponse)
async def update_processed_image(
    image_id: UUID,
    processed_url: str
):
    try:
        supabase = get_db()
        response = supabase.table('images').update({
            "processed_image_url": processed_url,
            "processed_at": "now()"
        }).eq('id', str(image_id)).execute()
        
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))