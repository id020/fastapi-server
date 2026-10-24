from typing import Literal

from pydantic import Field

from app.schemas.common import ORMModel


#
# 菜单请求模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 定义菜单名称、权限标识、菜单类型、路由及层级关系
#
class MenuInput(ORMModel):
    name: str = Field(min_length=1, max_length=100)
    permission: str = Field(min_length=1, max_length=160)
    menu_type: Literal["menu", "button"] = "menu"
    path: str = Field(default="", max_length=160)
    component: str = Field(default="", max_length=100)
    parent_id: int | None = None
    sort_order: int = Field(default=0, ge=0)


#
# 菜单基础信息响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 返回前端菜单导航及权限识别所需的基础字段
#
class MenuSummary(ORMModel):
    """向前端返回菜单导航所需的基础字段。"""

    id: int
    name: str
    permission: str
    menu_type: str
    path: str
    component: str
    parent_id: int | None
    sort_order: int


class MenuOutput(MenuSummary):
    pass
