from datetime import datetime

from pydantic import Field

from app.schemas import DepartmentOutput
from app.schemas.common import ORMModel
from app.schemas.role import RoleOutput


#
# 用户请求模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 定义用户账号、基本资料、所属部门及角色关联字段
#
class UserInput(ORMModel):
    username: str = Field(min_length=2, max_length=80)
    password: str | None = None
    nickname: str = Field(min_length=1, max_length=120)
    avatar: str | None = None
    status: bool = True
    department_id: int | None = None
    role_ids: list[int] = Field(default_factory=list)


#
# 用户基础信息响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 返回用户基础资料，不包含密码及密码哈希
#
class UserSummary(ORMModel):
    id: int
    username: str
    nickname: str
    avatar: str | None = None
    status: bool
    department_id: int | None


#
# 用户详情信息响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 返回用户基础资料、所属部门及角色关联字段
#
class UserDetail(UserSummary):
    # 所属部门：用户未关联部门时返回 None
    department: DepartmentOutput | None = None
    # 用户关联的角色 ID 列表
    role_ids: list[int] = Field(default_factory=list)

    # 用户关联的角色详情
    roles: list[RoleOutput] = Field(default_factory=list)

    # 创建时间和更新时间
    create_time: datetime | None = None
    update_time: datetime | None = None
