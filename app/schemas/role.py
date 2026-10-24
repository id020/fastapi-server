from pydantic import Field

from app.schemas.common import ORMModel


#
# 角色请求模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 定义角色名称、编码、数据权限范围及关联菜单和部门
#
class RoleInput(ORMModel):
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=255)
    data_scope: str = "self"
    menu_ids: list[int] = Field(default_factory=list)
    department_ids: list[int] = Field(default_factory=list)


#
# 角色响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 定义角色名称、编码、数据权限范围及关联菜单和部门
#
class RoleOutput(ORMModel):
    id: int
    name: str
    code: str
    description: str
    data_scope: str
    menu_ids: list[int] = Field(default_factory=list)
    department_ids: list[int] = Field(default_factory=list)
