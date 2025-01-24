import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test.settings')
django.setup(set_prefix=False)
###################################
from testDRF.models import Employee, Salary
from testDRF.serializers import EmployeeSerializer, SalarySerializer
import json

# mgr = Employee.objects

# 序列化
# 1 单一实例
# emp = mgr.get(pk=10004)  # Employee的一个实例
# serializer = EmployeeSerializer(emp)  # 传给构造器的第一参数是instance
# data = serializer.data  # 序列化，实例 => 字典
# print(type(data))  # ReturnDict
# print(data)
# print(json.dumps(data))  # 注意单引号和双引号的区别，字典 => json字符串

# 2 查询集
# emp = mgr.filter(pk__gt=10017)  # 查询集，多个实例
# serializer = EmployeeSerializer(emp, many=True)  # 使用many参数告诉序列化器给的是查询集
# data = serializer.data
# print(type(data))  # ReturnDict
# print(data)  # list[dict]
# print(*data, sep='\n')

# 反序列化
# 浏览器POST数据为JSON字符串，假设这里的data是已经被json处理过后的字典数据 json => 字典
# data = {'emp_no': 10018, 'birth_date': '1954-06-19', 'first_name': 'Kazuhide',
#         'last_name': 'Peha', 'gender': '2', 'hire_date': '1987-04-03'}
#
# serializer = EmployeeSerializer(data=data)  # 参数是data，不是instance
# serializer.is_valid()  # 校验
# # serializer.is_valid(raise_exception=True)  # 验证失败抛异常
# validated_data = serializer.validated_data  # 校验后准备入库的数据，注意和上面序列化的data的区别，data是返回给浏览器的数据
# print(type(validated_data))
# print(validated_data)

# 校验
# 1 序列化测试
# emp = mgr.get(pk=10004)
# emp.t1 = 't1'  # 不报错是因为是在is_valid()中校验
# emp.t2 = 't2'
# emp.t3 = 't3'  # 序列化不会输出
# serializer = EmployeeSerializer(emp)
# print(serializer.data)

# 2 反序列化测试
# data = {'emp_no': 10004, 'birth_date': '1954-05-01', 'first_name': 'Chirstian',
#         'last_name': 'Koblick', 'gender': 1, 'hire_date': '1986-12-01',
#         't1': 't111', 't2': 't2', 't3': 't3'}
# serializer = EmployeeSerializer(data=data)
# serializer.is_valid(raise_exception=True)
# print(serializer.validated_data)

# 入库
# 1 新增
# data = {'emp_no': 10022, 'birth_date': '1996-05-01', 'first_name': 'ming',
#         'last_name': 'xiao', 'gender': 1, 'hire_date': '2018-12-01', }
# serializer = EmployeeSerializer(data=data)  # 注意参数只有data没有instance，是新增
# serializer.is_valid(raise_exception=True)
# serializer.save()  # 返回了实例，调用了create
# print(serializer.validated_data)  # 校验后准备入库的数据

# 2 修改
# emp = mgr.get(pk=10021)
# data = {'emp_no': 10021, 'birth_date': '1996-05-01', 'first_name': 'san',
#         'last_name': 'zhang', 'gender': 1, 'hire_date': '2018-12-01', }
# serializer = EmployeeSerializer(instance=emp, data=data)  # 注意参数有instance，是更新
# serializer.is_valid(raise_exception=True)
# serializer.save()  # 返回了实例，调用了update
# print(serializer.validated_data)
# print(serializer.data)

# 下例是employees和salaries表的序列化操作
# 1 各自独立查询
emp = Employee.objects.get(emp_no=10003)
# print(emp)  # 不查询salaries表
# print(emp.salaries)  # 不查询salaries表，但可迭代
# print(emp.salaries.all())  # 会查询salaries表
# print('~' * 30)
# print(EmployeeSerializer(emp).data)  # instance -> dict
# print(SalarySerializer(emp.salaries.all(), many=True).data)  # 对结果集迭代封装

# 2 关联主键 PrimaryKeyRelatedField
# print(EmployeeSerializer(emp).data)  # 序列化器中定义了salaries属性，会查询salaries表

# 3 关联字符串表达 StringRelatedField
# print(EmployeeSerializer(emp).data)

# 4 关联对象
# print(json.dumps(EmployeeSerializer(emp).data))