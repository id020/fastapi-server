from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import api
from app.core.config import settings
from app.core.exceptions import register_exception_handlers

# ============================================================
# 1. 应用生命周期管理
# ============================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    管理 FastAPI 应用的启动和关闭。

    yield 之前：应用启动时执行。
    yield 之后：应用关闭时执行。

    后续可以在这里添加数据库连接检查、
    定时任务启动和资源释放等逻辑。
    """

    # ----------------------------
    # 应用启动时执行
    # ----------------------------
    print("FastAPI 应用启动")

    yield

    # ----------------------------
    # 应用关闭时执行
    # ----------------------------
    print("FastAPI 应用关闭")


# ============================================================
# 2. 创建静态文件目录（确保静态文件目录在挂载之前存在）
# ============================================================

settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 3. 创建 FastAPI 应用
# ============================================================

app = FastAPI(
    title="业务管理系统",
    description="基于 FastAPI 构建的业务管理后端 API",
    version="1.0.0",
    lifespan=lifespan,
)

# ============================================================
# 4. 挂载静态文件目录
# ============================================================

app.mount(
    "/uploads",
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)

# ============================================================
# 5. 配置跨域资源共享（CORS）
# ============================================================

# 开发环境允许 Vue 前端访问后端 API。
# 请根据实际前端开发服务器地址修改。
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 6. 注册异常处理器
# ============================================================

register_exception_handlers(app)


# ============================================================
# 7. 注册业务路由
# ============================================================

app.include_router(api)

# 后续创建路由文件后，在这里导入并注册。
#
# 例如：
# from app.api.v1.router import router as api_v1_router
# app.include_router(api_v1_router, prefix="/api/v1")


# ============================================================
# 8. 根路径接口
# ============================================================


@app.get("/", tags=["系统"])
def root():
    """
    根路径接口，用于检查应用是否正常响应。
    """

    return {
        "message": "实验室设备管理系统 API 运行正常",
        "version": "1.0.0",
    }


# ============================================================
# 9. 健康检查接口
# ============================================================


@app.get("/health", tags=["系统"])
def health_check():
    """
    检查应用进程是否可以正常响应。

    注意：这里只检查 API 是否能响应，
    并不代表数据库连接一定正常。
    """

    return {
        "status": "ok",
    }
