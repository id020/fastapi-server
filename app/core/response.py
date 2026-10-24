from typing import Any

from pydantic import BaseModel, Field

# ============================================================
# 1. 统一响应模型
# ============================================================


class Response(BaseModel):
    """
    统一 API 响应数据模型。

    用于规范后端接口返回的数据结构，确保前端能够以统一的方式
    获取业务状态码、提示信息和业务数据。

    字段说明：
        code: 业务状态码，用于标识本次操作的业务处理结果。
        message: 响应提示信息，通常用于向用户展示操作结果。
        data: 业务数据，可以是字典、列表、字符串、数字或其他数据。
              默认为 None，表示当前没有需要返回的业务数据。

    示例：
        {
            "code": 200,
            "message": "请求成功",
            "data": {"id": 1, "name": "张三"}
        }
    """

    # 业务状态码。
    # 例如：200 表示业务处理成功，400 表示业务请求错误，
    # 500 表示服务器内部业务处理失败。
    code: int

    # 响应提示信息，用于说明本次请求的处理结果。
    message: str

    # 业务数据，可以根据不同接口返回不同类型的数据。
    # 使用 Any 表示不限制具体的数据类型，默认值为 None。
    data: Any = None

    @classmethod
    def success(
        cls,
        message: str = "请求成功",
        data: Any = None,
    ) -> "Response":
        """
        构造统一的成功响应。

        参数：
            message: 成功提示信息，默认为“请求成功”。
            data: 需要返回给前端的业务数据，默认为 None。

        返回：
            Response: code 为 200 的统一响应对象。

        使用示例：
            return Response.success(data={"id": 1, "name": "张三"})

            return Response.success(
                message="查询成功",
                data=[{"id": 1}, {"id": 2}],
            )
        """
        return cls(
            code=200,
            message=message,
            data=data,
        )

    @classmethod
    def error(
        cls,
        code: int = 500,
        message: str = "请求失败",
    ) -> "Response":
        """
        构造统一的失败响应。

        参数：
            code: 业务错误码，默认为 500。
            message: 错误提示信息，默认为“请求失败”。

        返回：
            Response: 包含错误码和错误信息的统一响应对象。
                      由于没有传入 data，data 默认值为 None。

        使用示例：
            return Response.error(
                code=400,
                message="请求参数不正确",
            )

            return Response.error(
                code=404,
                message="未找到对应的用户",
            )
        """
        return cls(
            code=code,
            message=message,
        )


# ============================================================
# 2. 分页响应模型
# ============================================================


class PageResponse(BaseModel):
    """
    统一分页响应数据模型。

    用于返回列表查询、表格展示等分页接口的查询结果，
    将当前页的数据列表与符合查询条件的总记录数统一封装。

    字段说明：
        list: 当前页的数据列表，默认为空列表。
              通常存放用户列表、设备列表、实验室列表等数据。
        total: 符合查询条件的总记录数，默认为 0。
               该值通常用于前端计算总页数和展示分页组件。

    示例：
        {
            "list": [
                {"id": 1, "name": "张三"},
                {"id": 2, "name": "李四"}
            ],
            "total": 25
        }

    注意：
        total 表示符合查询条件的总记录数，而不是当前页的数据条数。
        list 只包含当前页实际返回的数据。
    """

    # 当前页的数据列表。
    # 使用 default_factory=list，为每个模型实例创建独立的空列表，
    # 避免多个实例共享可变的默认列表对象。
    list: Any = Field(default_factory=list)

    # 符合查询条件的总记录数，默认为 0。
    total: int = 0
