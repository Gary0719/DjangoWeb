from django.db import models

# Create your models here.


class Friend(models.Model):
    from_id = models.IntegerField(verbose_name='用户ID')
    to_id = models.IntegerField(verbose_name='好友ID')
    is_active = models.BooleanField(default=False,verbose_name='对方是否同意')
    class Meta:
        db_table = 'friends'
        verbose_name = '好友列表'
        verbose_name_plural = '好友列表'

class Letter(models.Model):
    letter = models.CharField(max_length=100,verbose_name='私信留言')
    sender = models.CharField(max_length=20,verbose_name='寄信人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    friend = models.ForeignKey(Friend)
    is_read = models.BooleanField(default=False,verbose_name='消息是否已读')
    class Meta:
        db_table = 'letters'
        verbose_name = '私信'
        verbose_name_plural = '私信'

    def __str__(self):
        return "%s:%s"%(self.sender,self.letter)

