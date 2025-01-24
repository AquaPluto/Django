from django.urls import path, include
# from .views import TestAPIView, EmpsView, EmpView, EmpViewSet
from .views import EmpViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()  # 内部构建了路由映射关系，路由表
router.register('emp/', EmpViewSet)  # 注册视图集
# urlpatterns = router.urls  # 没有其他路由可以这么写

urlpatterns = [
    # path('api/', TestAPIView.as_view()),  # /drf/api
    # path('course/<str:name>/<int:year>/', TestAPIView.as_view()),  # /drf/course/python/2025
    # path('emp/', EmpsView.as_view()),  # /drf/emp
    # path('emp/<int:pk>/', EmpView.as_view()),  # /drf/emp/10001

    # action：as.view({request.method: handler})
    # path('emp/', EmpViewSet.as_view({'get': 'list', 'post': 'create'})),  # /drf/emp/
    # path('emp/<int:pk>/', EmpViewSet.as_view({
    #     'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),  # /drf/emp/10001
] + router.urls  # 有其他路由这么写，list + list

print('+' * 30)
print(urlpatterns)
print('+' * 30)