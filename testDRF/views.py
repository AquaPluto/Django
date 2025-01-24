from rest_framework.views import APIView, Request, Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.mixins import (
    ListModelMixin,  # list -> 列表页get
    CreateModelMixin,  # create -> post
    RetrieveModelMixin,  # retrieve -> 详情页get
    UpdateModelMixin,  # update -> put, patch
    DestroyModelMixin  # destroy -> delete
)
from utils.paginations import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


# APIView
class TestAPIView(APIView):
    def get(self, request: Request, *args, **kwargs):  # request是DRF自己的request，重写
        print(f"method: {request.method}")  # 通过反射获得的属性，即HttpRequest的属性 request._request.mothod
        # print(request.GET)  # 查询字符串，HttpRequest的属性，推荐使用query_params
        print(request.query_params)  # 查询字符串，Request的属性
        print(request.query_params.get("x"))  # 有多个值返回最后一个，没有返回None
        print(request.query_params.getlist('x'))  # 取全部的值
        return Response({'Comment': "test Apiview get"})  # DRF自己的response，但继承自HttpResponse

    def post(self, request: Request, *args, **kwargs):
        print(request._request.body)  # 放在最前面，否则报错
        print(f"method: {request.method}")
        print(request.content_type)  # 表单提交的方法
        print(kwargs)  # url中的数据
        print(self.kwargs)  # handler内部使用 instance.post(request, **instance.kwargs)
        print(request.query_params)  # 查询字符串，Request的属性
        # print(request.POST)  # 表单提交的数据，HttpRequest的属性，推荐使用data
        print(request.data)  # Request的属性，使用小写的，包含提交的数据和文件，表单数据（多值字典），Json数据（字典）
        # return Response({'Comment': "test Apiview post"})
        return Response({
            'host': 'python', 'domain': 'magedu.com'
        }, status=201, headers={'X-Server': 'Magedu'})


# 列表页
# class EmpsView(APIView):
#     def get(self, request: Request, *args, **kwargs):
#         query_set = Employee.objects.all()
#         return Response(EmployeeSerializer(query_set, many=True).data)
#
#     def post(self, request: Request, *args, **kwargs):
#         serializer = EmployeeSerializer(data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.validated_data)


# 详情页
# class EmpView(APIView):
#     # 这些方法的关键字传参取决于 path('<int:id>/', EmpView.as_view()) 中<>有多少个参数
#     def get(self, request: Request, id=None):
#         query = Employee.objects.get(pk=id)
#         return Response(EmployeeSerializer(query).data)
#
#     def put(self, request: Request, id=None):
#         query = Employee.objects.get(pk=id)
#         serializer = EmployeeSerializer(instance=query, data=request.data)
#         serializer.is_valid()
#         serializer.save()
#         return Response(serializer.validated_data)
#
#     def delete(self, request: Request, id=None):
#         query = Employee.objects.get(pk=id)
#         query.delete()
#         return Response(status=204)

# GenericAPIView和Mixin
# class EmpsView(GenericAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#
#     # def get(self, request):
#     #     return ListModelMixin.list(self, request)
#     #     return self.list(request)  # 如果继承了ListModelMixin就可以这么写
#
#     # 可以发现get和ListModelMixin.list的参数一样，就有了更加简便的写法
#     get = ListModelMixin.list  # get(self, request) => ListModelMixin.list(self, request)
#
#     # def post(self, request):
#     #     return CreateModelMixin.create(self, request)
#
#     post = CreateModelMixin.create
#
#
# class EmpView(GenericAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     # lookup_url_kwarg = id  # 如果这里定义了id，那么path就要写'emp/<int:id>/'，如果不定义，就要写'emp/<int:pk>/'
#     get = RetrieveModelMixin.retrieve
#     put = UpdateModelMixin.update  # 所有字段，write_only必须都要有
#     # patch = UpdateModelMixin.partial_update  # 只提供个别字段
#     delete = DestroyModelMixin.destroy

# Concrete视图类
# class EmpsView(ListCreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer


# class EmpView(RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

# 分页
# class EmpsView(ListCreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     pagination_class = PageNumberPagination  # 单独指定自定义分页类，不使用全局，列表页专用

# 视图集
class EmpViewSet(ModelViewSet):
    # 通过内部是否使用pk来确定详情页还是列表页
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
