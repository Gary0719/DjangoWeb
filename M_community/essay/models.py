from django.conf import settings
from django.db import models

# Create your models here.
from user.models import User


class Essay(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    classify = models.CharField(max_length=1,verbose_name='话题')
    content = models.CharField(max_length=500,verbose_name='描述')
    image = models.ImageField(verbose_name='封面')
    author = models.ForeignKey(User,verbose_name='作者')
    video = models.CharField(max_length=100,verbose_name='视频URL',default='')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_active = models.BooleanField(default=True)
    click_rate = models.IntegerField(default=0,verbose_name='点击率')
    def __str__(self):
        return '%s %s %s'%(self.title,self.classify,self.author)
    class Meta:
        db_table = 'essay'
        verbose_name = '随笔'
        verbose_name_plural = '随笔'


class Comment(models.Model):
    comment = models.CharField(max_length=50,verbose_name='评论')
    the_essay = models.ForeignKey(Essay,verbose_name='文章')
    observer = models.ForeignKey(User,verbose_name='评论者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return '%s: %s'%(self.observer,self.comment)
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = '评论'