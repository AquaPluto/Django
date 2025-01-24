import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test.settings')
django.setup(set_prefix=False)
from testDjango.models import Book, Comment, Author

# print(*Book.__dict__.items(), sep='\n')
# print()
# print(*Comment.__dict__.items(), sep='\n')
# print()
# print(*Author.__dict__.items(), sep='\n')

# 新增操作
# 1 book表
for i in ['python', 'java', 'c++', 'nodejs']:
    Book.objects.create(**{"title": i})

# 2 comment表
Comment.objects.create(content="好简单", book=Book(pk=1))  # 使用实例传值，有风险，不确定是否有pk=1的数据
Comment.objects.create(content="有点难", book_id=2)  # 使用数据库字段传值，风险跟上例一样
Comment.objects.create(content="太难了", book=Book.objects.get(pk=3))  # 先去数据库查，有的话再赋值，推荐做法
Comment.objects.create(content="不是很难", book_id=Book.objects.get(pk=4).id)
Comment.objects.create(content="比较简单", book_id=Book.objects.get(pk=1).id)

# 3 author表
for n in ['Tom', "jerry", "Alex", 'wayne', "Sam"]:
    Author.objects.create(name=n)

# 4 author_book表
book = Book.objects.get(pk=1)
book.author_set.add(1)  # 新增author_id为1的数据
book.author_set.add(2)
book.author_set.set([1, 2, 3])  # 重置，这里Django发现1和2已经存在了，只添加3的
book.author_set.set([4, 5])
book = Book.objects.get(pk=2)
book.author_set.set([1, 2, 3])

# 查询操作
# 1 单表查询
# 1-1 查多条
b = Book.objects
print(b.all())
print(b.filter(pk__gt=2))
print(b.exclude(pk__gt=2))
print(b.count())

# 1-2 查一条
print(b.filter(pk=2))  # 返回集
print(b.get(pk=2))  # 单一对象，查不到抛异常
print(b.first())
print(b.last())
print(b.all()[:1])

# 2 一对多的查询
# 2-1 多端往一端查
c = Comment.objects.get(pk=1)
print(c.pk, c.created_time, c.content, c.book_id)  # 只会查comment表
print(c.pk, c.created_time, c.content, c.book)  # 因为book是Book的实例，包含所有字段，而comment表只有它的id，没有title，所以就会去再查book表（关联查询）

# 2-2 一端往多端查
b = Book.objects.get(pk=1)
print(b.pk, b.title, b.comment_set.filter(content__icontains="简单"))
print(b.comment_set.all())
print(b.comment_set.values('content'))

# 2-3 需求：查询python这本书籍的评论
c = Comment.objects  # 多端往一端查，查了3次，因为符合条件的数据有两条，就要去book表查两次
for x in c.filter(book_id=1):
    print(x.book.title, x.content)

b = Book.objects  # 一端往多端查，查了2次，推荐
for x in b.filter(id=1):
    for y in x.comment_set.filter(book_id=1):
        print(x.title, y.content)

# 3 多对多的查询（关联查询）
# 3-1 返回Author对象
print(Book.objects.get(pk=1).author_set.all())  # 查看id为1的这本书所有作者
print(Book.objects.get(pk=2).author_set.filter(pk__in=[1, 2]))  # 查看书本id为1的，作者id为1和2的作者，注意pk是author的pk
print(Author.objects.filter(pk=1, book__id=1))  # 查看书本id为1的对应的作者，且id为1的，book__id通过关系找字段，也可以写book__pk或者book

# 3-2 返回Book对象
print(Book.objects.filter(pk=2, author=2))  # 查看书本id为2，作者id为2的书本。author等价于author__id，通过关系找字段
print(Book.objects.filter(pk=2, author__id__gt=1))  # 查看书本id为2，作者id大于1的书本
print(Book.objects.filter(author__name="Tom"))  # 去找作者名为Tom的书本
print(Author.objects.get(pk=1).book.all())  # 去找作者名为Tom的书本
print(Author.objects.get(pk=1).book.filter(pk=1))  # 去找作者名为Tom，id为1的书本

# 更新操作
# 1 单一实例更新
book = Book.objects.get(pk=2)
book.title = "Java"
book.save()  # 有id是update，全体字段更新
book.save(update_fields=["title"])  # 指定字段更新

# 2 批量更新
Book.objects.filter(pk__gt=1).update(title="Java")

# 删除操作
# 1 单一实例删除
book = Book.objects.last()
book.delete()

# 2 批量删除
Book.objects.filter(pk__gt=2).delete()  # 批量删除，慎用
