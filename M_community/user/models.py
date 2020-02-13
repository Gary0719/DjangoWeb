from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16,verbose_name='用户名',unique=True)   #设置用户名为唯一主键,不能重复
    password = models.CharField(max_length=32,verbose_name='密码')
    gender = models.CharField(max_length=1,verbose_name='性别')   # 1或0,1为男生,0为女生
    email = models.EmailField(verbose_name='邮箱')
    head_portrait = models.ImageField(null=True,verbose_name='头像')  # 头像图片的存储路径,允许为空
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_active = models.BooleanField(default=False,verbose_name='是否激活')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return '用户:%s'%self.username

class WeiboUser(models.Model):
    uid = models.OneToOneField(User,null=True)	#与本网站用户表创建关联
    wuid = models.CharField(max_length=50,db_index=True)	#微博用户在微博的id
    access_token = models.CharField(max_length=100)
    class Meta:
        db_table = 'weibo_user'

    def __str__(self):
        return '%s %s'%(self.uid,self.wuid)