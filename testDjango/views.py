from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseNotFound, \
    HttpResponseNotAllowed, Http404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views import View
from django.utils.decorators import method_decorator
from random import randint
import datetime
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


# 视图函数
# 1 文本响应
def test_text(request: HttpRequest):
    data = 'Test String'  # WSGI对http请求报文使用env封装成字典
    return HttpResponse(data)  # 内部有默认的响应header，聚焦正文的生成，帮我们封装成response对象


# 2 Json响应
def test_json(request: HttpRequest):
    data = {"method": request.method, "path": request.path}
    return JsonResponse(data)  # content-type: application/json


# 3 限制请求方法
# 3-1 普通方法
def limit_method(request: HttpRequest):
    allowed_methods = ['get', 'post']
    if request.method.lower() in allowed_methods:
        return JsonResponse({"method": request.method, "path": request.path})
    else:
        return HttpResponse("Not allowed this method")
        # return HttpResponseForbidden()  # 403
        # return HttpResponseNotFound()  # 404
        # return HttpResponseNotAllowed(allowed_methods)  # 405
        # raise Http404


# 3-2 装饰器
# @require_http_methods(['GET', 'POST'])
# @require_GET
@require_POST
def decorate_limit(request: HttpRequest):
    data = {"method": request.method, "path": request.path}
    return JsonResponse(data)


# 视图类
# 请求方法
class TestView1(View):  # TestView1.as_view()返回的本质上还是handler函数
    def get(self, request):  # get方法
        data = {"method": request.method, "path": request.path}
        return JsonResponse(data)

    def post(self, request):  # post方法
        data = {"method": request.method, "path": request.path}
        return JsonResponse(data)


# 装饰器
# 1 装饰方法
# 1-1 第一种
class TestView2(View):
    # @method_decorator(require_GET)  # 允许get方法
    @method_decorator(require_http_methods(['GET', 'POST']))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        data = {"method": request.method, "path": request.path}
        return JsonResponse(data)

    def post(self, request):  # 如果装饰器没有允许该方法，写了也没用
        data = {"method": request.method, "path": request.path}
        return JsonResponse(data)


# 1-2 第二种
@method_decorator(require_GET, name="dispatch")  # 允许get方法
# @method_decorator(require_http_methods(['GET', 'POST']), name="dispatch")
class TestView3(View):
    def get(self, request):
        data = {"method": request.method, "path": request.path}
        return JsonResponse(data)

    def post(self, request):  # 如果装饰器没有允许该方法，写了也没用
        data = {"method": request.method, "path": request.path}
        return JsonResponse(data)


# 2 在路由配置中进行装饰

# session和cookie测试
def test_session(request: HttpRequest):
    # session测试
    print('+' * 30)
    print(type(request.session))
    sess: SessionStore = request.session  # session中间件加载的，是一个字典，存放客户端信息
    print(sess.items())
    sess['abc'] = str(randint(100, 200))  # 这个值存在服务端，和sessionid存在django_session表里
    print(sess.items())
    print(sess.session_key)  # sessionid，中间件负责把sessionid放在set-cookie
    print('+' * 30)
    # 使用sessionid查询数据库中session相关的数据
    s = Session.objects.get(pk='5qld747t6fylub4y4bpybm0fyc146b1l')
    print(s.expire_date)
    print(s.session_data)  # 序列化后的数据，就是sess.items()
    print(s.get_decoded())  # session_data反序列化后的数据
    print('+' * 30)
    # cookie测试
    res = JsonResponse({"text": "session"})
    res.cookies["time"] = "{:%H:%M:%S}".format(datetime.datetime.now())  # 响应报文增加cookie
    print(request.COOKIES)  # 从请求报文中提取所有的cookie键值对
    return res
