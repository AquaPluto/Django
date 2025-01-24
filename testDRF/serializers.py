from rest_framework import serializers
from .models import Employee, Salary
from functools import partial


# 字段级校验器（第二种写法）
# def validate_name(value, field_name='first_name', min=6, max=12):
#     print(f"{field_name}'s value is {value}")
#     if min <= len(value) <= max:
#         return value
#     raise serializers.ValidationError(f"The length must be between {min} and {max}")


# class EmployeeSerializer1(serializers.Serializer):
    # emp_no = serializers.IntegerField()
    # birth_date = serializers.DateField()
    # first_name = serializers.CharField(max_length=14)
    # last_name = serializers.CharField(max_length=16)
    # first_name = serializers.CharField()  # 字段级校验器测试（第一种写法）；对象级校验器测试
    # last_name = serializers.CharField()  # 字段级校验器测试（第一种写法）；对象级校验器测试
    # first_name = serializers.CharField(validators=[validate_name])  # 字段级校验器测试（第二种写法）
    # last_name = serializers.CharField(
    #     validators=[partial(validate_name, field_name='last_name', min=2, max=8)])  # 字段级校验器测试（第二种写法）
    # gender = serializers.ChoiceField(choices=Employee.Gender.choices)
    # hire_date = serializers.DateField()

    # 字段选项参数校验测试
    # t1 = serializers.CharField(min_length=4, max_length=8, required=False)
    # t2 = serializers.CharField(read_only=True)  # 序列化
    # t3 = serializers.CharField(write_only=True)  # 反序列化

    # 字段级校验器（第一种写法）
    # def validate_first_name(self, value):
    #     print(f"first_name's value is {value}")
    #     if 4 <= len(value) <= 10:
    #         return value
    #     raise serializers.ValidationError("The length must be between 4 and 10")
    #
    # def validate_last_name(self, value):
    #     print(f"last_name's value is {value}")
    #     if 4 <= len(value) <= 10:
    #         return value
    #     raise serializers.ValidationError("The length must be between 4 and 10")

    # 对象级校验器
    # def validate(self, attrs):
    #     print(type(attrs), attrs)  # dict
    #     first_name_value = attrs.get('first_name', "")
    #     if 4 <= len(first_name_value) <= 10:
    #         return attrs
    #     raise serializers.ValidationError("The length must be between 4 and 10")

    # 入库
    # def create(self, validated_data):
    #     return Employee.objects.using("testdrf").create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.birth_date = validated_data.get('birth_date', instance.birth_date)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.gender = validated_data.get('gender', instance.gender)
    #     instance.hire_date = validated_data.get('hire_date', instance.hire_date)
    #     instance.save(using="testdrf")
    #     return instance


# 模型序列化器
class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    # salaries必须和Model类中的属性对应，如果没有指定related_name，就是salaries_set
    # salaries=serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # 只读
    # salaries=serializers.PrimaryKeyRelatedField(many=True, queryset=Salary.objects.all())  # 可读写
    # salaries=serializers.StringRelatedField(many=True)  # 只读
    # salaries = SalarySerializer(many=True, read_only=True)  # 关联对象

    class Meta:
        model = Employee
        fields = '__all__'  # 指定所有字段

# print('~' * 30)
# print(EmployeeSerializer())  # 对于关系字段不会出现，即通过外键关联的字段
# print(SalarySerializer())
# print('~' * 30)
