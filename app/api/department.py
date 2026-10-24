from fastapi import APIRouter, Depends
from pymysql import IntegrityError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessException
from app.dependencies.permissions import require_permission
from app.models import Department, role_departments
from app.schemas.department import DepartmentInput, DepartmentOutput

router = APIRouter(prefix="/department", tags=["部门管理"])


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise BusinessException(message="提交失败") from exc


def _validate_parent(db: Session, department_id: int | None, parent_id: int | None):
    if parent_id is None:
        return
    if department_id == parent_id:
        raise BusinessException("上级部门不能是当前部门", code=422)

    parent = db.get(Department, parent_id)
    if parent is None:
        raise BusinessException("上级部门不存在", code=404)

    visited = set()
    while parent is not None:
        if parent.id == department_id:
            raise BusinessException("不能将部门移动到自己的下级部门", code=422)
        if parent.id in visited:
            raise BusinessException("部门层级已存在循环，请先修复数据", code=409)
        visited.add(parent.id)
        parent = db.get(Department, parent.parent_id) if parent.parent_id else None


@router.get(
    "/departments",
    response_model=list[DepartmentOutput],
    dependencies=[Depends(require_permission("departments:view"))],
)
def list_departments(db: Session = Depends(get_db)):
    return db.scalars(select(Department).order_by(Department.id)).all()


@router.get(
    "/departments/{department_id}",
    response_model=DepartmentOutput,
    dependencies=[Depends(require_permission("departments:view"))],
)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if department is None:
        raise BusinessException("部门不存在", code=404)
    return department


@router.post(
    "/departments",
    response_model=DepartmentOutput,
    dependencies=[Depends(require_permission("departments:write"))],
)
def create_department(payload: DepartmentInput, db: Session = Depends(get_db)):
    if not payload.name.strip():
        raise BusinessException("部门名称不能为空", code=422)
    _validate_parent(db, None, payload.parent_id)
    department = Department(
        name=payload.name.strip(),
        parent_id=payload.parent_id,
        description=payload.description.strip(),
    )
    db.add(department)
    _commit(db)
    db.refresh(department)
    return department


@router.put(
    "/departments/{department_id}",
    response_model=DepartmentOutput,
    dependencies=[Depends(require_permission("departments:write"))],
)
def update_department(
    department_id: int, payload: DepartmentInput, db: Session = Depends(get_db)
):
    department = db.get(Department, department_id)
    if department is None:
        raise BusinessException("部门不存在", code=404)
    if not payload.name.strip():
        raise BusinessException("部门名称不能为空", code=422)
    _validate_parent(db, department_id, payload.parent_id)
    department.name = payload.name.strip()
    department.parent_id = payload.parent_id
    department.description = payload.description.strip()
    _commit(db)
    db.refresh(department)
    return department


@router.delete(
    "/departments/{department_id}",
    dependencies=[Depends(require_permission("departments:write"))],
)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(Department, department_id)
    if department is None:
        raise BusinessException("部门不存在", code=404)

    role_count = db.scalar(
        select(func.count())
        .select_from(role_departments)
        .where(role_departments.c.department_id == department_id)
    )
    if department.children:
        raise BusinessException("该部门仍有下级部门，请先调整部门层级", code=409)
    if department.users:
        raise BusinessException("该部门仍有用户，请先调整用户所属部门", code=409)
    if role_count:
        raise BusinessException("该部门仍被角色授权，请先解除角色授权", code=409)

    db.delete(department)
    _commit(db)
    return {"message": "部门删除成功"}
