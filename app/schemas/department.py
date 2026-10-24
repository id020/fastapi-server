from pydantic import BaseModel, Field


#
# 部门请求模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 定义部门名称、上级部门及部门描述等字段
#
class DepartmentInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_id: int | None = None
    description: str = ""


#
# 部门响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 定义部门 ID、部门名称、上级部门 ID 及部门描述等字段
#
class DepartmentOutput(BaseModel):
    id: int
    name: str
    # 上级部门 ID，顶级部门为 None。
    parent_id: int | None = None
    description: str = ""
