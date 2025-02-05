from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional

class ImageBase(BaseModel):
    original_image_url: HttpUrl
    processed_image_url: Optional[HttpUrl] = None

class ImageCreate(ImageBase):
    user_id: UUID

class ImageResponse(ImageBase):
    id: UUID
    user_id: UUID
    uploaded_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True