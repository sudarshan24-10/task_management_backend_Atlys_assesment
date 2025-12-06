from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends, Response
from logger import Logger
from user.repository.db_mongo_repository import DbUserRepository
from user.service.user_service import UserService
from user.schema.user_schema import (
    UserCreateSchema, UserLoginSchema, UserResponseSchema
)
from auth.middleware.authentication_middleware import AuthBearer

logger = Logger().get_logger()

user_router = APIRouter(prefix="/auth", tags=["Users"])

@user_router.post("/register", response_model=UserResponseSchema, status_code=201)
async def register_user(
    user_data: UserCreateSchema,
    request: Request
) -> UserResponseSchema:
    try:
        logger.info("Register API called")
        db_session = request.app.state.db
        db_repository = DbUserRepository(db_session)
        user_service = UserService(db_repository)
        
        created_user = await user_service.create_user(user_data)
        return created_user
    except HTTPException as http_exc:
        logger.error(f"HTTPException in register_user route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in register_user route: {e}")
        raise HTTPException(status_code=500, detail="User registration failed")

@user_router.post("/login")
async def login_user(
    user_data: UserLoginSchema,
    request: Request,
    response: Response
):
    try:
        logger.info("Login API called")
        db_session = request.app.state.db
        db_repository = DbUserRepository(db_session)
        user_service = UserService(db_repository)
        
        login_response = await user_service.login_user(user_data)
        access_token = login_response.get("access_token")
        
        if access_token:
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="lax",
                max_age=3600
            )
        
        return {"message": "Login successful", "access_token": access_token}
    except HTTPException as http_exc:
        logger.error(f"HTTPException in login_user route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in login_user route: {e}")
        raise HTTPException(status_code=500, detail="User login failed")

@user_router.get("/me", response_model=UserResponseSchema)
async def get_current_user(
    authenticated_user = Depends(AuthBearer())
) -> UserResponseSchema:
    try:
        logger.info("Get current user route called")
        return authenticated_user
    except HTTPException as http_exc:
        logger.error(f"HTTPException in get_current_user route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_current_user route: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve current user")

@user_router.get("/users", response_model=List[UserResponseSchema])
async def get_all_users(
    request: Request,
    authenticated_user = Depends(AuthBearer())
):
    try:
        logger.info("Get all users route called")
        db_session = request.app.state.db
        db_repository = DbUserRepository(db_session)
        user_service = UserService(db_repository)
        
        users = await user_service.get_all_users()
        return users
    except HTTPException as http_exc:
        logger.error(f"HTTPException in get_all_users route: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Error in get_all_users route: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve users")
