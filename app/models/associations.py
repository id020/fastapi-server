from sqlalchemy import Table, Column, ForeignKey

from app.models.base import Base

# 用户与角色关联表：用于实现用户和角色之间的多对多关系
# 一个用户可以拥有多个角色，一个角色也可以分配给多个用户
user_roles = Table(
    "sys_user_roles",
    Base.metadata,
    # 用户 ID，关联 sys_users 表的 id；删除用户时级联删除关联记录
    Column("user_id", ForeignKey("sys_users.id", ondelete="CASCADE"), primary_key=True),
    # 角色 ID，关联 sys_roles 表的 id；删除角色时级联删除关联记录
    Column("role_id", ForeignKey("sys_roles.id", ondelete="CASCADE"), primary_key=True),
)


# 角色与菜单关联表：用于实现角色和菜单之间的多对多关系
# 一个角色可以拥有多个菜单权限，一个菜单也可以授权给多个角色
role_menus = Table(
    "sys_role_menus",
    Base.metadata,
    # 角色 ID，关联 sys_roles 表的 id；删除角色时级联删除关联记录
    Column("role_id", ForeignKey("sys_roles.id", ondelete="CASCADE"), primary_key=True),
    # 菜单 ID，关联 sys_menus 表的 id；删除菜单时级联删除关联记录
    Column("menu_id", ForeignKey("sys_menus.id", ondelete="CASCADE"), primary_key=True),
)


# 角色与部门关联表：用于配置角色的自定义数据权限范围
# 一个角色可以授权访问多个部门，一个部门也可以授权给多个角色
role_departments = Table(
    "sys_role_departments",
    Base.metadata,
    # 角色 ID，关联 sys_roles 表的 id；删除角色时级联删除关联记录
    Column("role_id", ForeignKey("sys_roles.id", ondelete="CASCADE"), primary_key=True),
    # 部门 ID，关联 sys_departments 表的 id；删除部门时级联删除关联记录
    Column(
        "department_id",
        ForeignKey("sys_departments.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
