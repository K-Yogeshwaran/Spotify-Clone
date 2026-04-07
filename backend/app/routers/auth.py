from fastapi import APIRouter, Depends, HTTPException, status
from app.supabase_client import sign_up, sign_in, sign_out, get_current_user
from app.schemas import Token, UserCreate, UserLogin, UserProfile, UserProfileUpdate
from app.services import user_profile


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate):
    try:
        response = await sign_up(payload.email, payload.password, payload.name)
        if response.user:
            return Token(access_token=response.session.access_token)
        else:
            raise HTTPException(status_code=400, detail="Signup failed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    try:
        response = await sign_in(payload.email, payload.password)
        if response.session:
            return Token(access_token=response.session.access_token)
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserProfile)
async def me():
    try:
        user = await get_current_user()
        if user:
            return UserProfile(
                id=user.id,
                email=user.email,
                name=user.user_metadata.get('name', user.email),
                created_at=user.created_at
            )
        else:
            raise HTTPException(status_code=401, detail="Not authenticated")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout():
    try:
        await sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
