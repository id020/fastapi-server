from fastapi import APIRouter, Depends
from pymysql import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessException
from app.dependencies.permissions import require_permission
from app.models import Menu
from app.schemas.menu import MenuInput, MenuOutput

router = APIRouter(prefix="/menu", tags=["菜单管理"])


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessException("权限标识已存在", code=409) from exc


def _validate_menu(db: Session, payload: MenuInput, menu_id: int | None = None):
    if not payload.name.strip() or not payload.permission.strip():
        raise BusinessException("名称和权限标识不能为空", code=422)
    if payload.menu_type == "menu" and (not payload.path.strip() or not payload.component.strip()):
        raise BusinessException("页面菜单必须填写路由路径和组件名称", code=422)
    if payload.menu_type == "menu" and not payload.path.strip().startswith("/"):
        raise BusinessException("页面菜单路由路径必须以 / 开头", code=422)
    if payload.menu_type == "button" and (payload.path.strip() or payload.component.strip()):
        raise BusinessException("按钮权限不应配置路由路径或组件名称", code=422)

    if payload.parent_id is None:
        return
    if menu_id == payload.parent_id:
        raise BusinessException("父级菜单不能是当前菜单", code=422)

    parent = db.get(Menu, payload.parent_id)
    if parent is None:
        raise BusinessException("父级菜单不存在", code=404)
    if parent.menu_type != "menu":
        raise BusinessException("按钮权限不能作为父级菜单", code=422)

    visited = set()
    while parent is not None:
        if parent.id == menu_id:
            raise BusinessException("不能将菜单移动到自己的下级菜单", code=422)
        if parent.id in visited:
            raise BusinessException("菜单层级已存在循环，请先修复数据", code=409)
        visited.add(parent.id)
        parent = db.get(Menu, parent.parent_id) if parent.parent_id else None


@router.get(
    "/menus",
    response_model=list[MenuOutput],
    dependencies=[Depends(require_permission("menus:view"))],
)
def list_menus(db: Session = Depends(get_db)):
    return db.scalars(select(Menu).order_by(Menu.sort_order, Menu.id)).all()


@router.get(
    "/menus/{menu_id}",
    response_model=MenuOutput,
    dependencies=[Depends(require_permission("menus:view"))],
)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise BusinessException("菜单不存在", code=404)
    return menu


@router.post(
    "/menus",
    response_model=MenuOutput,
    dependencies=[Depends(require_permission("menus:write"))],
)
def create_menu(payload: MenuInput, db: Session = Depends(get_db)):
    _validate_menu(db, payload)
    menu = Menu(
        name=payload.name.strip(),
        permission=payload.permission.strip(),
        menu_type=payload.menu_type,
        path=payload.path.strip(),
        component=payload.component.strip(),
        parent_id=payload.parent_id,
        sort_order=payload.sort_order,
    )
    db.add(menu)
    _commit(db)
    db.refresh(menu)
    return menu


@router.put(
    "/menus/{menu_id}",
    response_model=MenuOutput,
    dependencies=[Depends(require_permission("menus:write"))],
)
def update_menu(menu_id: int, payload: MenuInput, db: Session = Depends(get_db)):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise BusinessException("菜单不存在", code=404)
    if payload.menu_type == "button" and menu.children:
        raise BusinessException("该菜单仍有子项，不能改为按钮权限", code=409)
    _validate_menu(db, payload, menu_id)
    menu.name = payload.name.strip()
    menu.permission = payload.permission.strip()
    menu.menu_type = payload.menu_type
    menu.path = payload.path.strip()
    menu.component = payload.component.strip()
    menu.parent_id = payload.parent_id
    menu.sort_order = payload.sort_order
    _commit(db)
    db.refresh(menu)
    return menu


@router.delete(
    "/menus/{menu_id}", dependencies=[Depends(require_permission("menus:write"))]
)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.get(Menu, menu_id)
    if menu is None:
        raise BusinessException("菜单不存在", code=404)
    if menu.children:
        raise BusinessException("该菜单仍有子菜单，请先调整菜单层级", code=409)
    if menu.roles:
        raise BusinessException("该菜单仍被角色授权，请先解除角色授权", code=409)
    db.delete(menu)
    _commit(db)
    return {"message": "菜单删除成功"}
