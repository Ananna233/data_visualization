#HTML格式邮件
import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

if __name__ == '__main__':

    subject, from_email, to = '来自www.xxxxx.com的测试邮件', '3590746101@qq.com', '1476176620@qq.com'
    text_content = '欢迎访问www.xxxxx.com，这里是xx站点，专注于xx技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.baidu.com" target=blank>www.xxx.com</a>，这里是xx的站点，专注于xx技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

