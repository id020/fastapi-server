from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.department import router as department_router
from app.api.role import router as role_router
from app.api.menu import router as menu_router

api = APIRouter(prefix="/api")

api.include_router(auth_router)
api.include_router(user_router)
api.include_router(department_router)
api.include_router(role_router)
api.include_router(menu_router)
