from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


# 被发送者，发送标题，指定模板，传入模板的一组参数
def send_mail(to, subject, template, **kwargs):
    # msg = Message('赖还好', sender='814926605@qq.com', body='Test',
    #               recipients=['814926605@qq.com'])
    # 邮件标题，配置的邮箱，正文，接收者（列表，可以填入多个群发）
    msg = Message('[哈哈哈]' + '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()

