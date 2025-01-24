# HTTP通信原理
- 把客户端发送数据格式和服务器端响应返回数据格式等协商定义好，比如使用HTTP协议
- Client-Browser把请求封装成请求报文，通过`(ip:port)`发送给server
  - ip：主机到主机的信息路由
  - port：到了主机后找到对应的进程
- server服务进程绑定监听某个协议的某个端口，收到了Client-Browser发来的二进制数据，对数据进行校验，理解HTTP请求报文，对相应数据进行处理，最后相应的数据封装成HTTP响应报文返回
  - 请求数据如何处理？java框架、python框架、go框架等，也可以不使用框架
- Client-Browser收到响应报文并对其进行解析
# Django原理
## WSGI原理
- 浏览器：用户在浏览器中输入URL并发送HTTP请求。
- WSGI Server：接收来自浏览器的HTTP请求，并将其封装成一个字典environ，并调用app函数
  - 将environ作为第一参数传递给app函数
  - 提供第二参数`start_response`，作用是设置响应报文的状态码和响应头
  - `app(environ, start_response)`
- WSGI App：app函数的返回值是一个可迭代对象，每一个元素都是响应正文一部分，最后返回响应头和响应正文拼接而成的响应报文给WSGI Server
  - 在返回之前，必须先调用start_response来处理响应头
  - Django的本质就是app函数，响应正文正是我们需要写代码去处理的，
  - 比如通过中间件，路由映射到视图函数（类），然后再通过一次中间件，最终返回response
- WSGI Server接收到WSGI App返回的响应后，会将它封装为HTTP响应报文，并通过网络发送回浏览器
- 浏览器最终接收到这个HTTP响应报文，解析并渲染成相应的网页内容。
## Django视图基类View原理
- 在源码中，定义了http的方法的小写名称列表`http_method_names`
- View类中的`as_view()`方法，返回的是实际上就是视图函数view
  - 首先是实例化视图类，每一个请求到来都会创建一个视图类实例来处理该请求
  - 接着为实例增加了request属性
  - 返回dispatch函数，实际上真正的请求是被dispatch分发了
- dispatch函数
  - 提供与`request.method`对应的小写名称类中的实例方法
  - 然后在内部比对请求方法列表`http_method_names`，如果存在同名的get、post等方法，则调用同名的handler，否则返回405
## 中间件原理
- 在`settings.py`中的 MIDDLEWARE 配置着中间件的顺序
- 项目启动时会加载模块，即加载中间件列表，中间件列表中的所有中间件都会被实例化
- application被初始化的时候，即WSGIHanler实例化的时候，中间件初始化一次，初始化顺序和配置顺序相反，对应源码中的`self.load_middleware()`
- 按照配置顺序先后执行所有中间件的`get_response(request)`之前代码，即`process_request`，可以做请求之前拦截
- 全部执行完解析路径映射得到`view_func`
- `process_view`函数按照配置顺序依次向后执行。
  - 若是返回None，继续往后执行
  - 若是返回HttpResponse，就不会继续往后执行，直接返回response
- 执行view函数，前提是前面的所有中间件process_view都返回None
- 逆序执行所有中间件的`get_response(request)`之后代码，即`process_response`，可以做响应之前拦截
- 特别注意，若是在`get_response(request)`之前的代码返回HttpResponse，将从当前中间件立即返回该response，依次反弹返回response给浏览器端
# Django的ORM框架
- 不支持联合主键，只支持单一主键
- 在Model中定义的外键约束，是在Django应用层控制的，不管数据库层的外键约束是怎么样的
- 在一对多关系中，比如有员工表`Employee`和工资表`Salary`，工资表有一个外键字段`emp_no`，关联到员工表
  - 员工作为一端多了一个类属性`salary_set`，是一个查询集，可以使用`related_name`修改
  - 工资作为多端多了一个类属性`emp_no_id`，是数据库字段，可以使用`db_column`修改
  - `emp_no`是指向`Employee`的实例
  - 查询的时候最好从一端往多端查，否则会引起多次查询
- 在多对多关系中，比如员工表`Employee`和部门表`Department`
  - 在`Department`类中定义了指向`Employee`的字段，那么`Employee`就多了一个类属性`department_set`
  - 反之`Department`就多了一个类属性`employee_set`
# DRF原理
## 序列化器Serializer
序列化
- 将从数据库查询获得的实例转换为字典
  - 单个实例 => `dict`
  - 多个实例 => `list[dict]`
- `序列化器类实例.data`

反序列化
- 将浏览器的发送过来的数据经过json处理后转换的字典数据进行校验
- `序列化器类实例.is_valid()`
- validated_data是校验后准备入库的数据，注意和data的区别，data是返回给浏览器的数据
- 调用序列化器的`create,update,save`方法对校验过的数据入库，本质上用的是Model类写库
## 模型序列化器ModelSerializer
是Serializer的子类，除了具有Serializer的功能外，还具有以下功能
- 根据model类的字段和属性，自动生成序列化器的字段，属性和校验规则
- 如果校验规则比较复杂，需要自定义校验器
- 提供了`create,update,save`方法

Model的缺省管理器使用的就是default数据库配置，那么在多数据库的时候
- 可以通过自定义管理器来指定使用哪个数据库
- 如果有多个model类使用同一个管理器，或者同一个字段，可以使用Model抽象基类

在一对多或者多对多关系中，需要去获取关联字段，可以通过下列方法
- 关联主键：`PrimaryKeyRelatedField`
- 关联字符串：`StringRelatedField`
  - 内部`read_only`为`True`
- 关联对象：要利用对方的序列化器
## DRF视图
### APIView
APIView是DRF的视图类的基类，Django的View类是它的基类，它没有改变Django请求和响应的基本处理流程，我们最主要关注的是它提供的认证、授权功能
- `as_view()`调用基类View的，但是使用了`csrf_exempt(view)`来排除CSRF保护
- 重写了`dispatch()`，并没有改变原有的处理逻辑，还是用 `request.method.lower()` 去找handler
  - 对request的增强
    - 重新定义了Request类来替代Django的，实际上是利用了Django的request对象来构造DRF的request对象
    - 对请求进行认证和授权
    - DRF Request实例没有的属性利用反射，交给Django HttpRequest实例来处理
  - 对response的增强
    - 重新定义了Response类来增强替代Django的
    - 对序列化器生成的字典或者列表进行序列化，并返回response报文
  - 对异常处理的增强
    - 异常类都是基于APIException类的
- 没有提供增删改查的handler方法，需要自己定义get、post、put、delete方法
### 通用视图GenericAPIView
GenericAPIView提供了分页功能，为了解决APIView大量冗余的代码，提供了下列属性和方法
- **queryset**：类属性，默认为None，指定Model类及使用的管理器
- **serializer_class**：类属性，表示序列化类型，指定数据序列化和反序列化用的类
- get_queryset()：其内部默认使用类属性queryset，Mixin里面查数据集
- **get_object()**：详情页使用，其内部使用了get_queryset方法。Mixin里面获取单个对象调用它
- get_serializer_class()：返回值才是真正的被使用的序列化类，默认返回类属性serializer_class
- lookup_url_kwarg：定义path路径中的主键值对应的名，如果不定义默认使用 lookup_field 定义的pk

GenericAPIView没有提供增删改查，一样要自己写增删改查的代码，为了使增删改查的代码更加简便，需要Mixin其他类。
#### Mixins
- Mixins是实现孤立的功能Mixin类，需要和GenericAPIView类组合，以实现增删改查<br>
- 利用了写好的Mixin省掉了大量的增删改查代码。
#### Concrete视图类
- 原先我们需要定义小写的http方法，以处理请求，现在我们省略了增删改查的代码，也可以把定义http方法也省略掉，这就是Concrete视图类<br>
- Concrete视图类是由GenericAPIView和诸多Mixin类构成的子类。
### 视图集
- 使用Concrete视图类配置列表页和详情页，都是要定义GenericAPIView里面的类属性就行了，还是有重复的代码，那么视图集就可以简化<br>
- 视图集可以把列表页和详情页的视图代码合二为一，并且使用actions字典建立method到函数的映射
- SimpleRouter用来简化视图集的路由配置，解决复杂action的路径配置问题


