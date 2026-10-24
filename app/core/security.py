import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any
from app.core.config import settings

# ============================================================
# 1. 密码哈希工具
# ============================================================


def hash_password(password: str) -> str:
    """使用 bcrypt 为明文密码生成不可逆哈希。"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """安全比较登录密码与数据库中的 bcrypt 哈希。"""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ============================================================
# 2. 创建 JWT 访问令牌
# ============================================================


def create_access_token(
    user_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    """根据用户 ID 创建 JWT 访问令牌。"""

    # 获取当前 UTC 时间
    now = datetime.now(timezone.utc)

    # 计算令牌过期时间
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = now + expires_delta

    # 初始化 JWT 声明
    to_encode: dict[str, Any] = {
        "sub": str(user_id),
        "iat": now,
        "exp": expire,
    }

    # 使用密钥和指定算法对 Token 进行签名
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


# ============================================================
# 3. 验证 JWT 访问令牌
# ============================================================


def decode_access_token(token: str) -> int | None:
    """校验令牌签名和有效期，返回用户编号；无效令牌返回空值。"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={
                "require": ["exp", "sub"],
            },
        )

        # 如果解码成功，返回用户编号
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        # 如果解码失败，返回空值
        return None
