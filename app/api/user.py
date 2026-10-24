from operator import or_
from fastapi import APIRouter, Depends, Query
from pymysql import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.core.database import get_db
from app.core.exceptions import BusinessException
from app.core.security import hash_password
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_permission
from app.models import User, Role
from app.schemas.user import UserDetail, UserInput, UserSummary

router = APIRouter(prefix="/user", tags=["用户管理"])


def _commit(db: Session) -> None:
    """提交事务并将唯一键等数据库冲突转换为清晰的 HTTP 错误。"""
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessException(message="数据冲突，请检查名称、编码或关联数据") from exc


@router.get(
    "/users",
    response_model=list[UserDetail],
    dependencies=[Depends(require_permission("users:view"))],
)
def list_users(
        keyword: str | None = Query(default=None, max_length=50, description="用户名或昵称"),
        status: str | None = Query(default=None, description="账号状态：1启用，0停用"),
        db: Session = Depends(get_db)
):
    """获取用户列表，支持关键词和账号状态筛选"""

    query = db.query(User)

    # 1. 按用户名或昵称模糊搜索
    if keyword and keyword.strip():
        keyword = keyword.strip()
        search_pattern = f"%{keyword}%"

        query = query.filter(
            or_(
                User.username.ilike(search_pattern),
                User.nickname.ilike(search_pattern),
            )
        )

    # 2. 按账号状态筛选
    if status not in (None, ""):
        if status == "1":
            query = query.filter(User.status == True)
        elif status == "0":
            query = query.filter(User.status == False)

    # 3. 查询数据库
    users = query.all()

    # 4. 填充角色 ID
    for user in users:
        user.role_ids = [role.id for role in user.roles]

    return users


@router.get(
    "/{user_id}",
    response_model=UserDetail,
    dependencies=[Depends(require_permission("users:view"))],
)
def get_user_info(
        user_id: int,
        db: Session = Depends(get_db),
):
    """根据用户 ID 获取用户详情"""

    # 根据主键查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(code=404, message="用户不存在")

    user.role_ids = [role.id for role in user.roles]
    return user


@router.post(
    "",
    response_model=UserSummary,
    dependencies=[Depends(require_permission("users:write"))],
)
def create_user(payload: UserInput, db: Session = Depends(get_db)):
    """创建用户并设置部门、角色及初始密码。"""
    if not payload.password:
        raise BusinessException(code=422, message="新建用户必须设置密码")

    if not payload.avatar:
        payload.avatar = "https://www.gravatar.com/avatar/default?d=identicon"

    # 批量查询角色
    roles = list(db.scalars(select(Role).where(Role.id.in_(payload.role_ids))).all())

    if len(roles) != len(set(payload.role_ids)):
        raise BusinessException(code=404, message="角色不存在")

    item = User(
        username=payload.username,
        nickname=payload.nickname,
        avatar=payload.avatar,
        password=hash_password(payload.password),
        status=payload.status,
        department_id=payload.department_id,
        roles=roles,
    )

    db.add(item)
    _commit(db)
    db.refresh(item)

    return item


@router.put("/{user_id}", dependencies=[Depends(require_permission("users:write"))])
def update_user(
        user_id: int,
        payload: UserInput,
        db: Session = Depends(get_db),
        actor: User = Depends(get_current_user),
):
    """更新用户资料和角色；密码字段有值时才重新设置密码。"""

    if not user_id:
        raise BusinessException(code=422, message="用户 ID 不能为空")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise BusinessException(code=404, message="用户不存在")

    # 检查当前登录用户是否为当前用户或是否停用当前用户
    if user.id == actor.id and not payload.status:
        raise BusinessException(code=422, message="不能停用当前登录账号")

    # 批量查询角色
    roles = list(db.scalars(select(Role).where(Role.id.in_(payload.role_ids))).all())

    if len(roles) != len(set(payload.role_ids)):
        raise BusinessException(code=404, message="角色不存在")

    user.username, user.nickname = payload.username, payload.nickname
    user.status, user.department_id = payload.status, payload.department_id
    user.role_ids = payload.role_ids

    if payload.avatar:
        user.avatar = payload.avatar

    if payload.password:
        user.password = hash_password(payload.password)

    _commit(db)
    db.refresh(user)

    return user
