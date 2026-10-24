from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, foreign

from app.models.associations import user_roles
from app.models.base import TimestampBase

if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.role import Role


#
# 用户ORM模型
#
# @author: allen
# @date: 2026-10-10
# @version: 1.0
# @description: 用户ORM模型
#
class User(TimestampBase):
    """保存登录账号、密码哈希、所属部门和用户角色关联。"""

    __tablename__ = "sys_users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(80), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(120), nullable=False)
    avatar: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    department_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # 所属部门
    department: Mapped[Department | None] = relationship(
        "Department",
        # 放在这里TYPE_CHECKING的，需要使用字符串类型， 因为此时TYPE_CHECKING还没有加载，所以无法使用Department类型
        primaryjoin="foreign(User.department_id) == Department.id",
        back_populates="users",
        uselist=False,
    )

    # 用户角色
    roles: Mapped[list[Role]] = relationship(
        "Role", secondary=user_roles, back_populates="users"
    )
