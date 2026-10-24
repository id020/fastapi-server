#
# ORM 模型统一导出模块
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 统一导出系统 ORM 模型，方便其他模块引用及数据库表注册
#

from app.models.base import Base
from app.models.associations import (
    user_roles,
    role_menus,
    role_departments,
)

from app.models.user import User
from app.models.department import Department
from app.models.menu import Menu
from app.models.role import Role

__all__ = [
    "Base",
    "user_roles",
    "role_menus",
    "role_departments",
    "User",
    "Department",
    "Menu",
    "Role",
]
