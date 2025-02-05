from app.core.config import Settings
from typing import Optional
from supabase import create_client, Client
from app.errors.custom_exceptions import DatabaseError

settings = Settings()

class Database:
    """Singleton class to manage Supabase client connection"""
    _instance: Optional[Client] = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Returns a Supabase client instance using the Singleton pattern.
        
        Returns:
            Client: Supabase client instance
            
        Raises:
            DatabaseError: If environment variables are not properly configured
        """
        if cls._instance is None:
            url = settings.supabase_url
            key = settings.supabase_key
            
            if not url or not key:
                raise DatabaseError(
                    "SUPABASE_URL and SUPABASE_KEY environment variables must be set"
                )
            
            try:
                cls._instance = create_client(url, key)
            except Exception as e:
                raise DatabaseError(f"Failed to initialize Supabase client: {str(e)}")
                
        return cls._instance

def get_db() -> Client:
    """
    Utility function to get the Supabase client instance.
    
    Returns:
        Client: Supabase client instance
    """
    return Database.get_client()