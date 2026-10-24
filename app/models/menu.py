from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base
from app.models.associations import role_menus

if TYPE_CHECKING:
    from app.models.role import Role


#
# 菜单ORM模型
#
# @author: allen
# @date: 2026-10-10
# @version: 1.0
# @description: 菜单ORM模型
#
class Menu(Base):
    """菜单模型：用于存储系统的菜单、页面、按钮和 API 权限信息。"""

    __tablename__ = "sys_menus"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    permission: Mapped[str] = mapped_column(
        String(160), nullable=False, unique=True, index=True
    )
    menu_type: Mapped[str] = mapped_column(String(16), nullable=False, default="menu")
    path: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    component: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("sys_menus.id"), nullable=True
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    parent: Mapped[Menu | None] = relationship(
        "Menu", remote_side="Menu.id", back_populates="children"
    )
    children: Mapped[list[Menu]] = relationship(
        "Menu", back_populates="parent", cascade="save-update, merge"
    )

    # 关联角色：菜单与角色之间是多对多关系
    # 一个角色可以拥有多个菜单或权限，一个菜单或权限也可以分配给多个角色
    roles: Mapped[list[Role]] = relationship(
        "Role",
        secondary=role_menus,
        back_populates="menus",
    )
