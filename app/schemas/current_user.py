from pydantic import BaseModel

from app.schemas import UserSummary, MenuSummary


#
# 当前用户信息响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 返回当前用户基本资料、权限标识列表及菜单列表
#
class CurrentUserResponse(BaseModel):
    user: UserSummary
    permissions: list[str]
    menus: list[MenuSummary]
