from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.permissions import require_permission
from app.models import Role
from app.schemas.role import RoleOutput

router = APIRouter(prefix="/role", tags=["角色管理"])


#
# 查询所有角色
#
# 返回字段：
# id             角色 ID
# name           角色名称
# code           角色编码
# description    角色描述
# data_scope     数据权限范围
# menu_ids       当前角色关联的菜单 ID 列表
# department_ids 当前角色关联的部门 ID 列表
@router.get(
    "/roles",
    response_model=list[RoleOutput],
    dependencies=[Depends(require_permission("roles:view"))],
)
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    for role in roles:
        role.menu_ids = [m.id for m in role.menus]
        role.department_ids = [d.id for d in role.departments]
    return roles
