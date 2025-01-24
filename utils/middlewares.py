from django.http import HttpResponse


# MagMiddleware1(get_response)(request) --> response
class MagMiddleware1:
    def __init__(self, get_response):
        """每一个中间件被初始化一次"""
        print(self.__class__.__name__, "init~~~~")
        self.get_response = get_response  # 实例化一次

    # MagMiddleware1(get_response)实例化 等价为 MagMiddleware1(下一层函数)
    # 中间件实例(request) -> response
    def __call__(self, request):
        # request请求在去视图的路上
        # process_request
        print(1, self.__class__.__name__, "__call__ start ~~~~")
        # request中的内容也可以被拦截，就不需要return HttpResponse
        # 比如做ip检测：if ip 不是在一定的范围，阻止你，连进入视图的机会都不给
        # return HttpResponse(self.__class__.__name__) # 测试点1

        response = self.get_response(request)  # 内层函数(request)等返回
        # 内层函数是谁？调用链上的下一级，可能是中间件实例，或是视图函数
        # self.get_response表示下一层

        # 内层函数调用完成返回response的路上
        # process_response
        print(2, self.__class__.__name__, "__call__ finish #####")
        # return HttpResponse("我是MagMiddleware1返回路上") # 替换返回结果,若response出现异常.就返回HttpResponse
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """调用视图前被调用，返回值是None不影响当前处理流程，继续向后执行，是HttpResponse对象就不往后执行"""
        print(5, self.__class__.__name__, "process_view~~~~",
              view_func.__name__, view_args, view_kwargs)
        # return HttpResponse(self.__class__.__name__ + ' process_view') # 测试点3


class MagMiddleware2:
    def __init__(self, get_response):
        """执行一次"""
        print(self.__class__.__name__, "init~~~~")
        self.get_response = get_response

    def __call__(self, request):
        # request请求去视图的路上
        print(3, self.__class__.__name__, "__call__ start ~~~~")
        # return HttpResponse(self.__class__.__name__) # 测试点2

        # 内层函数调用完成返回response的路上
        response = self.get_response(request)
        print(4, self.__class__.__name__, "__call__ finish #####")
        # return HttpResponse("我是MagMiddleware2返回路上") # 测试点5
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """调用视图前被调用，返回值是None或HttpResponse对象"""
        print(6, self.__class__.__name__, "process_view~~~~",
              view_func.__name__, view_args, view_kwargs)
        # return HttpResponse(self.__class__.__name__ + ' process_view') # 测试点4
