from django.core.mail import send_mail
from M_community.celery import app


@app.task
def send_active_email(url,email):
    '''
    使用celery队列进行邮件的发送,防止网络传输的阻塞
    :param url:
    :param email:
    :return:
    '''
    subject = '喵の社区激活邮件'
    html_message = '''
    <h3>尊敬的用户您好,欢迎您加入喵の社区:</h3>
    <div>
    <p>
        &nbsp;&nbsp;为确保您在本社区后续功能的正常体验,请点击链接,对您的邮箱进行激活☞<a href='%s' target=blank>点击激活</a>,该链接十分钟内有效,请尽快进行操作.
    </p>
    </div>'''%url
    send_mail(subject=subject,message='',from_email='3345416463@qq.com',recipient_list=[email],html_message=html_message)
    print('邮件发送成功')