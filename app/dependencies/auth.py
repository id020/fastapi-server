from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models import User

# 创建 Bearer Token 解析器。
#
# 客户端通常需要在请求头中携带：
# Authorization: Bearer 实际的Token字符串
#
# auto_error=False 表示认证信息缺失或无法按预期解析时，
# 不立即由 HTTPBearer 自动返回错误，而是交给下面的
# get_current_user() 统一处理并返回自定义错误信息。
bearer_scheme = HTTPBearer(auto_error=False)


# 定义系统允许使用的数据范围。
#
# self：
#   本人数据。当前查询过滤函数通过默认条件实现本人记录可见。
#
# department：
#   本部门数据。当前示例查询逻辑会加入用户所属部门的记录。
#
# department_tree：
#   本部门及下级部门数据。
#
# custom：
#   自定义部门数据。通过角色关联的部门确定授权范围，
#   当前实现还会包含这些部门的下级部门。
#
# all：
#   全部数据，不添加当前示例记录的数据范围过滤条件。
DATA_SCOPES = {
    "self",
    "department",
    "department_tree",
    "custom",
    "all",
}


def get_current_user(
    # 从请求头中获取 Bearer 认证凭证。
    #
    # HTTPAuthorizationCredentials | None 表示：
    # credentials 可能是认证凭证，也可能是 None。
    #
    # Depends(bearer_scheme) 表示由 FastAPI 自动执行
    # bearer_scheme，并将解析结果传给 credentials。
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    # 获取当前请求使用的数据库会话。
    # Depends(get_db) 会调用项目中的 get_db() 获取 Session。
    db: Session = Depends(get_db),
) -> User:
    """
    获取当前登录用户。

    执行步骤：
    1. 检查请求是否携带 Bearer Token。
    2. 解析 Token，获取用户 ID。
    3. 根据用户 ID 从数据库查询用户。
    4. 检查用户是否存在、账号是否启用。
    5. 返回当前用户对象。

    如果认证失败或账号已停用，则抛出 HTTP 401 错误。
    """

    # 如果没有提供认证凭证，说明请求没有携带有效的 Bearer 认证信息。
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="请先登录")

    # 获取 Token 字符串，并交给安全模块解析。
    # 如果 Token 无效或过期，具体如何处理取决于
    # decode_access_token() 的实现。
    #
    # 假设解析成功，user_id 可能为用户主键，例如 1。
    # 如果解析失败且函数以 None 表示失败，则 user_id 为 None。
    user_id = decode_access_token(credentials.credentials)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录状态无效或账号已停用",
        )

    user: User | None = db.get(User, user_id)

    if user is None or not user.status:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录状态无效或账号已停用",
        )

    return user
