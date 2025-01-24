from django.db import models


# 自定义管理器
class MyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('testdrf')


class AbstractBaseModel(models.Model):
    objects = MyManager()

    class Meta:
        abstract = True  # 抽象基Model类，表明不和表对应，不能实例化


class Employee(AbstractBaseModel):
    class Meta:
        db_table = 'employees'

    # 枚举类型，用于限定性别字段的取值范围
    # 第一个值是存储在数据库中的整数值，第二个值是显示给用户的字符串。
    class Gender(models.IntegerChoices):
        MAN = 1, '男'
        WOMAN = 2, '女'

    # 定义模型字段
    emp_no = models.IntegerField(primary_key=True, verbose_name='员工编号')  # 主键，由于不是自增id主键字段，所以要定义主键
    birth_date = models.DateField(verbose_name='出生日期')
    first_name = models.CharField(max_length=14, verbose_name='名')
    last_name = models.CharField(max_length=16, verbose_name='姓')
    gender = models.SmallIntegerField(default=1, choices=Gender.choices, verbose_name='性别')
    hire_date = models.DateField(verbose_name='入职日期')

    # 定义属性方法，用于获取员工全名
    @property
    def name(self):
        return "[{} {}]".format(self.last_name, self.first_name)

    # 定义repr方法，用于返回员工的字符串表示形式
    def __repr__(self):
        return "< E {} {} >".format(self.emp_no, self.name)

    __str__ = __repr__


class Salary(AbstractBaseModel):
    class Meta:
        db_table = "salaries"

    # id = models.AutoField(primary_key=True) # 额外增加的主键，Django不支持联合主键
    emp_no = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='emp_no',
                               related_name='salaries')  # 注册在Employee中的属性名
    from_date = models.DateField()
    salary = models.IntegerField(verbose_name='工资')
    to_date = models.DateField()

    def __str__(self):
        return f"{self.pk}:{self.salary}"
