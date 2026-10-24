from pydantic import BaseModel, ConfigDict


#
# ORM 响应模型基类
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 允许响应模型直接读取 SQLAlchemy ORM 对象属性
#
class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
