from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class MagBaseAPIException(APIException):
    """基类定义基本的异常"""
    code = 10000  # code为0表示正常，非0表示错误
    message = '非法请求'  # 错误描述

    @classmethod  # 使用类方法，方便调用get_message方法
    def get_message(cls):
        return {'code': cls.code, 'message': cls.message}


class MyZeroDivisionError(MagBaseAPIException):
    code = 1
    message = '除零异常'


class MyDoesNotExist(MagBaseAPIException):
    code = 2
    message = '找不到数据'


# 内部异常暴露细节，替换为自定义，异常映射表
# 异常名 : 异常类 based MagBaseAPIException
exc_map = {
    'ZeroDivisionError': MyZeroDivisionError,
    'DoesNotExist': MyDoesNotExist
}


def global_exception_handler(exc, context):
    # exc：捕获到的异常对象。
    # context：包含异常上下文信息的字典。
    """
    全局异常处理
    不管什么异常这里统一处理。根据不同类型显示不同的信息
    为了前端JS解析方便，这里响应的状态码采用默认的200
    异常对应处理后返回对应的错误码和错误描述
    异常找不到对应就返回缺省MagBaseAPIException
     """
    print(exc, type(exc))  # division by zero <class 'ZeroDivisionError'>
    print(exc.__class__.__name__)  # ZeroDivisionError
    # 在这里可以进行日志记录，或写入elasticsearch
    errmsg = exc_map.get(exc.__class__.__name__,
                         MagBaseAPIException).get_message()  # 在exc_map中如果找不到ZeroDivisionError对应的处理异常类，就交给基类处理
    response = Response(errmsg, status=200)  # 状态恒为200
    return response
