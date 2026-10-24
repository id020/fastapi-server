from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import relationship, foreign, Mapped, mapped_column

from app.models.base import Base
from app.models.associations import (
    user_roles,
    role_menus,
    role_departments,
)

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.menu import Menu
    from app.models.department import Department


#
# 角色ORM模型
#
# @author: allen
# @date: 2026-10-10
# @version: 1.0
# @description: 角色ORM模型
#
class Role(Base):

    __tablename__ = "sys_roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    code: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    data_scope: Mapped[str] = mapped_column(String(32), nullable=False, default="self")

    # 角色关联的用户：多对多
    users: Mapped[list[User]] = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
    )

    # 角色关联的菜单：多对多
    menus: Mapped[list[Menu]] = relationship(
        "Menu",
        secondary=role_menus,
        back_populates="roles",
    )

    # 角色授权的数据部门：多对多
    departments: Mapped[list[Department]] = relationship(
        "Department",
        secondary=role_departments,
    )
