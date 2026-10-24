from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.permissions import require_permission
from app.models import Department
from app.schemas.department import DepartmentOutput

router = APIRouter(prefix="/department", tags=["部门管理"])


#
# 获取所有部门列表
# 功能说明：
# 1. 查询数据库中的所有部门。
# 2. 按部门 ID 升序排列。
# 3. 返回部门 ID、名称、上级部门 ID 和描述。
# 4. 前端可以根据 parent_id 构建树形部门结构。
#
# 权限要求：
# 当前用户必须具有 departments:view 权限。
#
# 返回示例：
# [
#     {
#         "id": 1,
#         "name": "研发部",
#         "parent_id": null,
#         "description": "负责产品研发"
#     },
#     {
#         "id": 2,
#         "name": "后端开发组",
#         "parent_id": 1,
#         "description": "负责后端服务开发"
#     }
# ]
@router.get(
    "/departments",
    response_model=list[DepartmentOutput],
    dependencies=[Depends(require_permission("departments:view"))],
)
def list_departments(db: Session = Depends(get_db)):
    # 查询数据库中的所有部门，并按部门 ID 升序排列
    return db.query(Department).order_by(Department.id).all()
