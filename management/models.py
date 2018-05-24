from django.db import models


# Create your models here.

# 出版社表
class Publisher(models.Model):
    name = models.CharField(max_length=64, verbose_name="作者")
    email = models.EmailField(null=True, verbose_name="出版社邮箱")
    added_at = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return '<Publisher {}>'.format(self.name)

    class Meta:
        verbose_name = "出版社表"
        db_table = "publisher"
        ordering = ("id",)


# 作者表
class Author(models.Model):
    name = models.CharField(max_length=64, verbose_name="作者")
    status = models.BooleanField(verbose_name="状态", default="1")
    added_at = models.DateTimeField(verbose_name="添加时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    def __str__(self):
        return '<Author {}>'.format(self.name)

    class Meta:
        verbose_name = "作者表"
        db_table = "author"
        ordering = ("id",)


# 作者详情表
class AuthorInfo(models.Model):
    GENDER_CHOICES = (
        (0, u'保密'),
        (1, u'男'),
        (2, u'女'),
    )
    DYNASTY_CHOICES = (
        (0, u'未知'),
        (1, u'现代'),
        (2, u'清'),
        (3, u'明'),
    )
    author = models.OneToOneField(to='Author', related_name="info", on_delete=models.CASCADE, verbose_name="作者ID")
    avatar = models.CharField(max_length=128, default='avatar/default.png', verbose_name="头像")
    birthday = models.DateField(verbose_name="生日")
    gender = models.SmallIntegerField(verbose_name="性别", choices=GENDER_CHOICES, default=GENDER_CHOICES[0])
    dynasty = models.SmallIntegerField(verbose_name="朝代", choices=DYNASTY_CHOICES, default=DYNASTY_CHOICES[0])
    native = models.CharField(max_length=64, null=True, verbose_name="籍贯")

    class Meta:
        verbose_name = "作者详情表"
        db_table = "author_info"


# 图书表
class Book(models.Model):
    name = models.CharField(max_length=64, verbose_name="书名")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    number = models.IntegerField(default=1, verbose_name="存量")
    info = models.TextField(null=True, verbose_name="图书简介")
    status = models.BooleanField(verbose_name="状态", default="1")
    author = models.ManyToManyField(to=Author, related_name="book_authors", verbose_name="图书作者")
    publisher = models.ForeignKey(to=Publisher, null=True, on_delete=models.CASCADE, related_name="book_publishers",
                                  verbose_name="出版社")
    added_at = models.DateTimeField(verbose_name="上架时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        verbose_name = "图书表"
        db_table = "book"
        ordering = ("id",)