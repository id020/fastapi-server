from pydantic import BaseModel


#
# 用户登录请求模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 接收用户登录时提交的账号和密码
#
class LoginRequest(BaseModel):
    username: str
    password: str


#
# JWT 令牌响应模型
#
# @author: allen
# @date: 2026-10-22
# @version: 1.0
# @description: 返回访问令牌
#
class TokenResponse(BaseModel):
    access_token: str
