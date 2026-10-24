import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# ============================================================
# 1. 数据库连接地址
# ============================================================

# 从配置文件中获取数据库连接地址，配置文件可以读取.env 文件。
DATABASE_URL = settings.DATABASE_URL

# ============================================================
# 2. 创建数据库引擎
# ============================================================

# engine 负责管理数据库连接，并通过连接池复用连接。
# 它不是某一次具体的数据库会话。
#
# pool_pre_ping=True：
# 每次从连接池取出连接时，检查连接是否仍然有效，
# 可以减少使用到失效连接的情况。
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# 3. 创建 Session 工厂
# ============================================================

# SessionLocal 是一个 Session 工厂，而不是一个 Session 实例。
#
# 每次调用 SessionLocal()，都会创建一个新的数据库会话。
#
# autoflush=False：
# 不在每次查询前自动 flush，避免隐式写入时机难以理解。
#
# expire_on_commit=False：
# 提交事务后，不自动将 ORM 对象的属性标记为过期。
# 这样提交后仍可以读取已加载的属性。
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# ============================================================
# 4. 获取数据库会话的依赖函数
# ============================================================


def get_db():
    """
    为一次请求提供独立的数据库会话。

    yield 将 Session 提供给调用方使用。
    请求依赖结束后，finally 会执行 db.close()，
    归还连接池中的连接并释放 Session 资源。

    注意：
    close() 不等于 commit()。
    是否提交或回滚事务，应由业务代码明确管理。
    """

    # 创建一个新的数据库会话
    db: Session = SessionLocal()

    try:
        # 将数据库会话交给 FastAPI 的 Depends 使用
        yield db

    finally:
        # 无论请求成功还是发生异常，都关闭会话
        db.close()
