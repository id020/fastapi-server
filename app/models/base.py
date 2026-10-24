from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ============================================================
# 一、定义基础 ORM 模型基类
# ============================================================


class Base(DeclarativeBase):
    """
    所有 ORM 模型的基础类。

    所有实际数据库模型都继承该类。
    默认提供 id 主键字段。
    """

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID"
    )


# ============================================================
# 二、定义带创建时间和更新时间的基类
# ============================================================


class TimestampBase(Base):
    """
    带时间字段的抽象 ORM 基类。

    继承该类的模型自动拥有：
    1. id：主键ID
    2. create_time：创建时间
    3. update_time：更新时间

    __abstract__ = True 表示该类本身不对应数据库表。
    """

    # 声明为抽象基类，不单独映射数据库表
    __abstract__ = True

    # 创建时间
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="创建时间",
    )

    # 更新时间
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        comment="更新时间",
    )
