from supabase import create_client, Client
from app.config import settings
import os

# Validate Supabase configuration
if not settings.supabase_url or not settings.supabase_key:
    raise ValueError(
        "Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.\n"
        "1. Create a Supabase project at https://supabase.com\n"
        "2. Get your Project URL and Service Role Key from Settings > API\n"
        "3. Update your .env file with these credentials"
    )

# Initialize Supabase client
try:
    supabase: Client = create_client(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key
    )
    print(f"Supabase client initialized successfully for project: {settings.supabase_url[:30]}...")
except Exception as e:
    raise ValueError(f"Failed to initialize Supabase client: {str(e)}")

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    return supabase

# Authentication helpers
async def sign_up(email: str, password: str, name: str = None):
    """Sign up a new user"""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name or email.split('@')[0]
                }
            }
        })
        return response
    except Exception as e:
        raise Exception(f"Sign up failed: {str(e)}")

async def sign_in(email: str, password: str):
    """Sign in a user"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        raise Exception(f"Sign in failed: {str(e)}")

async def sign_out():
    """Sign out current user"""
    try:
        response = supabase.auth.sign_out()
        return response
    except Exception as e:
        raise Exception(f"Sign out failed: {str(e)}")

async def get_current_user():
    """Get current authenticated user"""
    try:
        response = supabase.auth.get_user()
        return response.user if response.user else None
    except Exception as e:
        raise Exception(f"Get current user failed: {str(e)}")

# Database helpers
async def create_table(table_name: str, data: dict):
    """Create a record in Supabase table"""
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response
    except Exception as e:
        raise Exception(f"Create {table_name} failed: {str(e)}")

async def get_table(table_name: str, filters: dict = None):
    """Get records from Supabase table"""
    try:
        query = supabase.table(table_name)
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response
    except Exception as e:
        raise Exception(f"Get {table_name} failed: {str(e)}")

async def update_table(table_name: str, record_id: int, data: dict):
    """Update a record in Supabase table"""
    try:
        response = supabase.table(table_name).update(data).eq('id', record_id).execute()
        return response
    except Exception as e:
        raise Exception(f"Update {table_name} failed: {str(e)}")

async def delete_table(table_name: str, record_id: int):
    """Delete a record from Supabase table"""
    try:
        response = supabase.table(table_name).delete().eq('id', record_id).execute()
        return response
    except Exception as e:
        raise Exception(f"Delete {table_name} failed: {str(e)}")
