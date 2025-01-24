from django.db import models


class Book(models.Model):
    class Meta:
        db_table = 'book'

    # id 现在默认为bigint，默认主键
    title = models.CharField(max_length=100)

    # comment_set
    # author_set

    def __repr__(self):
        return '<Book {}-{}>'.format(self.pk, self.title)

    __str__ = __repr__


class Comment(models.Model):
    # 1:n 1本书有n条评论，1条评论针对1本书。用外键
    class Meta:
        db_table = 'comment'

    created_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=512)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Book的实例
    # book_id  数据库字段


class Author(models.Model):
    # n:n 1本书有多个作者，1个作者有多本书。创建第3张表
    class Meta:
        db_table = 'author'

    # 没有through参数和自定义模型，Django会自动创建第三张表
    book = models.ManyToManyField(Book)
    name = models.CharField(max_length=128, null=False)
