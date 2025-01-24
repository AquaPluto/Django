from django.urls import path
from testDjango.views import test_text, test_json, limit_method, decorate_limit, TestView1, TestView2, TestView3, \
    test_session
from django.views.decorators.http import require_GET, require_http_methods

urlpatterns = [
    path('text/', test_text),  # /django/text
    path('json/', test_json),
    path('limit/', limit_method),
    path('decorate/', decorate_limit),
    path('TestView1/', TestView1.as_view()),
    path('TestView2/', TestView2.as_view()),
    path('TestView3/', TestView3.as_view()),
    # path('TestView1/', require_GET(TestView1.as_view())),  # 装饰器装饰
    # path('TestView1/', require_http_methods(['POST'])(TestView1.as_view())),  # 装饰器装饰
    path('session/', test_session),
]
