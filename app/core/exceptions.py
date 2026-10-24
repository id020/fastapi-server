from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# ============================================================
# 1. 自定义业务异常及其处理器
# ============================================================


class BusinessException(Exception):
    """自定义业务异常，用于处理业务逻辑中的预期错误。"""

    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(message)


async def business_exception_handler(
    request: Request,
    exc: Exception,
):
    if not isinstance(exc, BusinessException):
        raise exc

    """统一处理自定义业务异常，并返回约定的 JSON 响应格式。"""
    return JSONResponse(
        status_code=200,
        content={
            "code": exc.code,
            "message": str(exc.message),
            "data": None,
        },
    )


# ============================================================
# 2. HTTP 异常处理
# ============================================================


async def http_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    统一处理 FastAPI 的 HTTP 异常。

    常见场景：
    - 401：未通过身份认证。
    - 403：没有访问资源的权限。
    - 404：请求的资源不存在。
    - 其他：根据异常中的 HTTP 状态码返回对应错误信息。
    """

    if not isinstance(exc, HTTPException):
        raise exc

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": str(exc.detail),
            "data": None,
        },
        headers=exc.headers,
    )


# ============================================================
# 3. 请求参数校验异常处理器
# ============================================================


async def validation_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    统一处理请求数据校验失败的异常。

    常见场景：
    - 缺少必填参数。
    - 参数类型不符合要求。
    - 请求参数不符合 Pydantic 模型定义的校验规则。

    仅向客户端返回字段位置和错误原因，不返回用户提交的原始值，
    以减少敏感信息泄露的风险。
    """

    if not isinstance(exc, RequestValidationError):
        raise exc

    # 提取字段位置和错误原因，不向前端返回用户提交的原始值
    errors = [
        {
            "field": ".".join(str(item) for item in error["loc"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "请求参数校验失败",
            "data": errors,
        },
    )


# ============================================================
# 4. 全局未处理异常处理器
# ============================================================


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    统一处理未被其他异常处理器捕获的意外异常。

    处理原则：
    - 在服务器日志中记录异常信息及完整堆栈，便于排查问题。
    - 向客户端返回通用错误信息。
    - 不向客户端暴露异常堆栈、数据库连接信息等内部细节。
    """

    # 记录完整异常堆栈，方便开发人员排查问题
    import logging

    logger = logging.getLogger(__name__)
    logger.exception(
        "系统发生未处理异常：%s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None,
        },
    )


# ============================================================
# 5. 注册全局异常处理器
# ============================================================


def register_exception_handlers(app: FastAPI) -> None:
    """
    为 FastAPI 应用统一注册异常处理器。

    根据异常类型，将请求过程中发生的异常交给对应的处理器处理，
    统一错误响应的数据结构，方便前端进行错误提示和处理。
    """

    # 处理自定义业务异常
    app.add_exception_handler(
        BusinessException,
        business_exception_handler,
    )

    # 处理 HTTP 异常
    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    # 处理请求参数校验异常
    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    # 处理其他未被专门处理的异常
    app.add_exception_handler(
        Exception,
        global_exception_handler,
    )
