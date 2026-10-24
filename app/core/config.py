from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    项目配置类。

    默认从项目根目录的 .env 文件读取配置。
    环境变量的优先级高于 .env 文件中的同名配置。
    """

    # ============================
    # 1. 数据库配置
    # ============================

    # 数据库连接地址
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/my_database"

    # ============================
    # 2. JWT 身份认证配置
    # ============================

    # JWT 签名密钥
    # 正式环境必须通过环境变量设置强随机密钥
    SECRET_KEY: str = "replace-this-with-a-random-secret-key"

    # JWT 签名算法
    ALGORITHM: str = "HS256"

    # 访问令牌有效期，单位：分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ========================================================
    # 3. 文件上传配置
    # ========================================================

    # 上传文件保存目录
    # 默认保存到 backend/uploads/
    UPLOAD_DIR: Path = BASE_DIR / "uploads"

    # 单个文件最大允许上传大小，单位：字节
    # 100 * 1024 * 1024 = 100 MB
    MAX_FILE_SIZE: int = 100 * 1024 * 1024

    # 允许上传的文件后缀
    # 使用小写，校验时统一将文件后缀转换为小写
    ALLOWED_EXTENSIONS: set[str] = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".zip",
    }

    # ============================
    # 4. 配置文件读取规则
    # ============================

    model_config = SettingsConfigDict(
        # .env 文件路径
        env_file=".env",
        # .env 文件使用 UTF-8 编码
        env_file_encoding="utf-8",
        # 环境变量名称不区分大小写
        case_sensitive=False,
        # 忽略 .env 中不属于本配置类的额外字段
        extra="ignore",
    )


# 创建全局配置对象，其他模块直接导入 settings 使用
settings = Settings()
