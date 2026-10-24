#
# Schema 模型统一导出模块
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 统一导出 API 请求、响应及公共数据模型
#

from app.schemas.common import ORMModel
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.department import DepartmentInput, DepartmentOutput
from app.schemas.role import RoleInput
from app.schemas.menu import MenuInput, MenuSummary
from app.schemas.user import UserInput, UserSummary
from app.schemas.current_user import CurrentUserResponse

__all__ = [
    "ORMModel",
    "LoginRequest",
    "TokenResponse",
    "DepartmentInput",
    "DepartmentOutput",
    "RoleInput",
    "MenuInput",
    "MenuSummary",
    "UserInput",
    "UserSummary",
    "CurrentUserResponse",
]
