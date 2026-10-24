from collections.abc import Callable
from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session, Query
from starlette import status

from app.dependencies.auth import get_current_user, DATA_SCOPES
from app.models import User, Department


def user_permissions(user: User) -> set[str]:
    """
    汇总当前用户拥有的全部权限编码。

    一个用户可以关联多个角色；
    一个角色又可以关联多个菜单或权限项。

    遍历用户的所有角色，收集每个角色关联的
    menu.permission，并以集合 set 的形式返回。

    例如：
        {
            "users:view",
            "users:write",
            "records:view"
        }

    返回 set 可以自动去除重复的权限编码。
    """

    # 等价于：
    #
    # permissions = set()
    # for role in user.roles:
    #     for menu in role.menus:
    #         permissions.add(menu.permission)
    # return permissions
    #
    # user.roles：当前用户关联的角色集合。
    # role.menus：当前角色关联的菜单及权限项。
    # menu.permission：具体的权限编码。
    return {menu.permission for role in user.roles for menu in role.menus}


def require_permission(permission: str) -> Callable:
    """
    创建一个检查指定权限编码的依赖函数。

    参数：
        permission：接口要求的权限编码。
                    例如 "users:view" 或 "users:write"。

    返回：
        内部函数 check。

    使用方式：
        Depends(require_permission("users:write"))

    FastAPI 会执行返回的 check 函数。
    check 会先获取当前用户，再判断用户是否拥有所需权限。
    """

    # 定义内部权限检查函数。
    #
    # user 参数通过 Depends(get_current_user) 获取。
    # FastAPI 会先执行 get_current_user()，
    # 将验证通过的用户对象传给 user。
    def check(user: User = Depends(get_current_user)) -> User:

        # 获取用户所有权限编码，并检查接口要求的权限
        # 是否存在于用户的权限集合中。
        if permission not in user_permissions(user):

            # 身份认证通过但没有操作权限，返回 HTTP 403。
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权执行此操作",
            )

        # 用户具备要求的权限，返回当前用户。
        # 如果接口需要知道当前操作者是谁，也可以使用该返回值。
        return user

    # 返回内部函数，而不是直接执行 check()。
    #
    # 这样 require_permission("users:write")
    # 就可以作为 Depends() 的参数使用。
    return check


def descendant_department_ids(db: Session, root_id: int) -> set[int]:
    """
    获取指定部门及其所有下级部门的 ID。

    参数：
        db：数据库会话。
        root_id：要查询的根部门 ID。

    返回：
        包含根部门自身及所有下级部门 ID 的集合。

    示例：
        总部 ID=1
        ├── 研发部 ID=2
        └── 销售部 ID=3

        调用 descendant_department_ids(db, 1)
        返回 {1, 2, 3}。

    使用场景：
        当角色的数据范围是 department_tree 或 custom 时，
        需要根据部门的 parent_id 关系找到所有下级部门。
    """

    # found 保存已经发现的部门 ID。
    # 初始化时先将根部门自身加入结果集合。
    #
    # 使用集合可以避免同一个部门 ID 被重复添加。
    found = {root_id}

    # pending 保存尚未查询下级部门的部门 ID。
    # 初始只需要处理根部门。
    pending = [root_id]

    # 只要还有待处理的部门，就继续查询。
    while pending:

        # pending.pop() 从尾部取出一个待处理的部门 ID。
        #
        # 查询所有直接隶属于该部门的子部门。
        # Department.parent_id 表示当前部门的上级部门 ID。
        #
        # .all() 返回查询结果列表。
        children = (
            db.query(Department.id).filter(Department.parent_id == pending.pop()).all()
        )

        # 解包，查询结果中的每一项是一个只包含 ID 的元组。
        # 例如：[(2,), (3,)]。
        for (child_id,) in children:

            # 如果这个子部门尚未处理，就将其加入结果集合，
            # 同时放入 pending，后续继续查找它的下级部门。
            if child_id not in found:
                found.add(child_id)
                pending.append(child_id)

    # 返回根部门以及所有找到的下级部门 ID。
    return found


def get_user_data_scope(db: Session, user: User) -> tuple[bool, set[int]]:
    """
    计算用户的数据范围。

    返回：
        (是否拥有全部数据权限, 可访问的部门 ID 集合)

    说明：
        具体的本人数据条件由业务模块根据自己的所有者字段添加。
    """

    # 获取当前用户关联的全部角色。
    roles = user.roles

    # 任意一个角色拥有全部数据权限，就可以访问全部数据。
    if any(role.data_scope == "all" for role in roles):
        return True, set()

    # 如果没有角色拥有全部数据权限，就需要根据角色的 data_scope
    # 来计算用户可访问的部门范围。
    department_ids: set[int] = set()

    # 遍历用户的所有角色，合并各角色允许访问的部门范围。
    for role in roles:
        # 情况一：仅允许访问本人所属部门的数据。
        if role.data_scope == "department" and user.department_id is not None:
            # 将当前用户所属部门加入授权部门集合。
            department_ids.add(user.department_id)

        # 情况二：允许访问本人所属部门及其所有下级部门。
        elif role.data_scope == "department_tree" and user.department_id is not None:
            # 获取当前用户部门及其下级部门，并合并到集合中。
            department_ids.update(descendant_department_ids(db, user.department_id))

        # 情况三：允许访问角色自定义授权的部门。
        elif role.data_scope == "custom":
            # role.departments 表示该角色关联的授权部门。
            for department in role.departments:
                # 将每个授权部门及其所有下级部门加入集合。
                department_ids.update(descendant_department_ids(db, department.id))

    return False, department_ids


def apply_record_data_scope(
    query: Query,
    db: Session,
    user: User,
    *,
    owner_column: Any,
    department_column: Any,
):
    """
    为任意业务查询添加数据范围过滤条件。

    参数：
        query：
            已构造的 SQLAlchemy 查询对象。

        db：
            数据库会话。

        user：
            当前登录用户。

        owner_column：
            业务模型中代表记录所有者的字段。
            例如 Equipment.created_by。

        department_column：
            业务模型中代表所属部门的字段。
            例如 Equipment.department_id。

    规则：
        1. all：不限制数据范围。
        2. 本人创建的数据始终允许查询。
        3. department：增加本部门的数据。
        4. department_tree：增加本部门及下级部门的数据。
        5. custom：增加自定义授权部门的数据。
        6. 多个角色的数据范围取并集。
    """

    # 获取用户的数据范围。
    all_data, department_ids = get_user_data_scope(db, user)

    # 如果用户拥有全部数据权限，直接返回原始查询，不添加数据范围限制。
    if all_data:
        return query

    # 本人创建的记录。
    clauses = [owner_column == user.id]

    # 授权部门内的记录。
    if department_ids:
        clauses.append(department_column.in_(department_ids))

    # 本人记录 OR 授权部门记录。
    return query.filter(or_(*clauses))


def can_access_department(db: Session, user: User, department_id: int) -> bool:
    """
    判断当前用户是否可以访问指定部门。

    主要用于创建或转移示例业务记录时，
    检查目标部门是否在当前用户允许操作的范围内。

    参数：
        db：数据库会话。
        user：当前登录用户。
        department_id：目标部门 ID。

    返回：
        True：当前函数判定允许访问。
        False：当前函数判定不允许访问。

    注意：
        本函数判断的是部门访问范围，不等于完整的 API 权限校验。
        调用方还应根据业务需要检查对应的操作权限。
    """

    # 如果用户任意一个角色的数据范围是 all，
    # 则允许访问任意目标部门。
    if any(role.data_scope == "all" for role in user.roles):
        return True

    # 如果目标部门恰好是用户自己的所属部门，
    # 当前实现会直接允许访问。
    #
    # 注意：这是现有代码的具体规则，即使角色没有 department
    # 数据范围，也会触发此判断。
    if user.department_id == department_id:
        return True

    # 逐个检查用户的角色。
    for role in user.roles:

        # 情况一：角色具有 department_tree 数据范围。
        if role.data_scope == "department_tree" and user.department_id is not None:

            # 获取用户所属部门及其所有下级部门。
            # 如果目标部门位于其中，则允许访问。
            if department_id in descendant_department_ids(db, user.department_id):
                return True

        # 情况二：角色具有 custom 数据范围。
        if role.data_scope == "custom":

            # allowed 保存当前角色允许访问的部门 ID。
            allowed = set()

            # 遍历角色授权的部门。
            for department in role.departments:

                # 将每个授权部门及其下级部门加入允许集合。
                allowed.update(descendant_department_ids(db, department.id))

            # 如果目标部门在当前角色允许的范围内，则通过。
            if department_id in allowed:
                return True

    # 所有角色检查完毕，仍未找到允许访问的依据。
    return False


def validate_data_scope(value: str) -> str:
    """
    校验数据范围配置是否合法。

    参数：
        value：待校验的数据范围字符串。

    返回：
        合法时返回原始字符串。
        不合法时抛出 HTTP 422 错误。

    使用场景：
        创建角色或修改角色时，
        检查提交的 data_scope 是否属于系统支持的范围。
    """

    # 如果提交的值不在预定义的数据范围集合中，
    # 说明这是一个不受支持的配置。
    if value not in DATA_SCOPES:

        # 返回 HTTP 422，提示调用方可以使用哪些合法值。
        raise HTTPException(
            status_code=422,
            detail=(f"data_scope 必须为：" f"{', '.join(sorted(DATA_SCOPES))}"),
        )

    # 校验通过，返回原值，方便调用方直接使用或保存。
    return value
