from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, foreign

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.user import User


#
# 部门ORM模型
#
# @author: allen
# @date: 2026-10-10
# @version: 1.0
# @description: 部门ORM模型
#
class Department(Base):
    __tablename__ = "sys_departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    # 上级部门
    parent: Mapped["Department"] = relationship(
        "Department",
        primaryjoin=lambda: foreign(Department.parent_id) == Department.id,
        remote_side="Department.id",
        back_populates="children",
    )

    # 下级部门：当前部门下面的所有子部门
    children: Mapped["Department"] = relationship(
        "Department",
        primaryjoin=lambda: Department.id == foreign(Department.parent_id),
        back_populates="parent",
        # ORM 级联操作配置：
        # all 表示级联多种 ORM 操作，例如保存、更新、删除等
        # delete-orphan 表示子部门脱离父部门后，如果满足孤儿条件，
        # SQLAlchemy 会在 flush 时删除该子部门记录
        # 注意：删除父部门时，也可能级联删除其子部门
        cascade="all, delete-orphan",
    )

    # 部门下的用户：当前部门所属的所有用户
    users: Mapped[list[User]] = relationship(
        "User",
        # 放在这里TYPE_CHECKING的，需要使用字符串类型， 因为此时TYPE_CHECKING还没有加载，所以无法使用User类型
        primaryjoin="Department.id == foreign(User.department_id)",
        back_populates="department",
    )
