from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessException
from app.core.security import verify_password, create_access_token
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import user_permissions
from app.models import User
from app.schemas import (
    TokenResponse,
    LoginRequest,
    CurrentUserResponse,
    UserSummary,
    MenuSummary,
)

router = APIRouter(prefix="/auth", tags=["权限认证"])


# 用户登录
@router.post("/login", response_model=TokenResponse, summary="用户登录")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """校验账号密码并签发单 JWT 访问令牌。"""
    user: User | None = db.query(User).filter(User.username == payload.username).first()
    if (
        user is None
        or not user.status
        or not verify_password(payload.password, user.password)
    ):
        raise BusinessException(code=401, message="用户名或密码错误")
    return TokenResponse(access_token=create_access_token(user.id))


# Dashboard首页面板
@router.get("/me", response_model=CurrentUserResponse, summary="查询当前用户")
def current_user_info(user: User = Depends(get_current_user)) -> CurrentUserResponse:
    """返回当前用户、其角色权限码和可见菜单。"""
    permissions = user_permissions(user)
    menus = sorted(
        (
            menu
            for role in user.roles
            for menu in role.menus
            if menu.menu_type == "menu"
        ),
        key=lambda menu: (menu.sort_order, menu.id),
    )
    # 多角色可能共同授予同一菜单，按菜单编号去重后再返回导航树原始节点。
    unique_menus = {menu.id: menu for menu in menus}
    return CurrentUserResponse(
        user=UserSummary.model_validate(user),
        permissions=sorted(permissions),
        menus=[MenuSummary.model_validate(menu) for menu in unique_menus.values()],
    )
