from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db

from app.schemas.user import UserResponse, UserCreate
from app.schemas.token import Token

from app.services.user_service import create_user, authenticate_user

from app.core.security import create_access_token
from app.core.deps import get_current_user

from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await create_user(db, user_data)
        return user
    except ValueError:
        raise HTTPException(status_code=400, detail="Данный пользователь уже существует!")


@router.post("/login", response_model=Token)
async def login_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user