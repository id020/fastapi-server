from fastapi import APIRouter, Depends
from pymysql import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessException
from app.dependencies.permissions import require_permission, validate_data_scope
from app.models import Department, Menu, Role
from app.schemas.role import RoleInput, RoleOutput

router = APIRouter(prefix="/role", tags=["角色管理"])


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessException(message="提交失败") from exc


def _role_output(role: Role) -> Role:
    role.menu_ids = [menu.id for menu in role.menus]
    role.department_ids = [department.id for department in role.departments]
    return role


def _resolve_ids(db: Session, model, ids: list[int], label: str):
    unique_ids = set(ids)
    rows = list(db.scalars(select(model).where(model.id.in_(unique_ids))).all())
    if len(rows) != len(unique_ids):
        raise BusinessException(f"所选{label}中包含不存在的记录", code=422)
    return rows


@router.get(
    "/roles",
    response_model=list[RoleOutput],
    dependencies=[Depends(require_permission("roles:view"))],
)
def list_roles(db: Session = Depends(get_db)):
    roles = db.scalars(select(Role).order_by(Role.id)).all()
    return [_role_output(role) for role in roles]


@router.get(
    "/roles/{role_id}",
    response_model=RoleOutput,
    dependencies=[Depends(require_permission("roles:view"))],
)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.get(Role, role_id)
    if role is None:
        raise BusinessException("角色不存在", code=404)
    return _role_output(role)


@router.post(
    "/roles",
    response_model=RoleOutput,
    dependencies=[Depends(require_permission("roles:write"))],
)
def create_role(payload: RoleInput, db: Session = Depends(get_db)):
    if not payload.name.strip() or not payload.code.strip():
        raise BusinessException("角色名称和编码不能为空", code=422)
    validate_data_scope(payload.data_scope)
    departments = (
        _resolve_ids(db, Department, payload.department_ids, "部门")
        if payload.data_scope == "custom"
        else []
    )
    role = Role(
        name=payload.name.strip(),
        code=payload.code.strip(),
        description=payload.description.strip(),
        data_scope=payload.data_scope,
        menus=_resolve_ids(db, Menu, payload.menu_ids, "菜单权限"),
        departments=departments,
    )
    db.add(role)
    _commit(db)
    db.refresh(role)
    return _role_output(role)


@router.put(
    "/roles/{role_id}",
    response_model=RoleOutput,
    dependencies=[Depends(require_permission("roles:write"))],
)
def update_role(role_id: int, payload: RoleInput, db: Session = Depends(get_db)):
    role = db.get(Role, role_id)
    if role is None:
        raise BusinessException("角色不存在", code=404)
    if not payload.name.strip() or not payload.code.strip():
        raise BusinessException("角色名称和编码不能为空", code=422)
    validate_data_scope(payload.data_scope)
    departments = (
        _resolve_ids(db, Department, payload.department_ids, "部门")
        if payload.data_scope == "custom"
        else []
    )
    role.name = payload.name.strip()
    role.code = payload.code.strip()
    role.description = payload.description.strip()
    role.data_scope = payload.data_scope
    role.menus = _resolve_ids(db, Menu, payload.menu_ids, "菜单权限")
    role.departments = departments
    _commit(db)
    db.refresh(role)
    return _role_output(role)


@router.delete(
    "/roles/{role_id}", dependencies=[Depends(require_permission("roles:write"))]
)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.get(Role, role_id)
    if role is None:
        raise BusinessException("角色不存在", code=404)
    if role.users:
        raise BusinessException("该角色仍分配给用户，请先解除用户关联", code=409)
    db.delete(role)
    _commit(db)
    return {"message": "角色删除成功"}
