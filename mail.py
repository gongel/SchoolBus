import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from future.backports.email.mime.text import MIMEText

#
# class Mail:
#     def __call__(self, uuid, status, qrcode):
#         send_QR(uuid, status, qrcode)


def send_QR(qrcode):
    print('准备发送二维码')
    sender = '18516528861@163.com'  #
    passWord = 'gel12345'
    mail_host = 'smtp.163.com'
    # receivers是邮件接收人，用列表保存，可以添加多个
    receivers = ['higongel@gmail.com']
    # 设置email信息
    msg = MIMEMultipart()
    # 邮件主题
    msg['Subject'] = 'WeChat QR'
    # 发送方信息
    msg['From'] = sender
    # 邮件正文是MIMEText:
    # msg_content = '尽快扫码吧！'
    # 简单文本到正文，plain
    # msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
    # 将附件图片嵌入正文，html
    msg.attach(MIMEText('<html><body>' + '<p><img src="cid:0"></p>' + '</body></html>', 'html', 'utf-8'))
    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    # with open(qrcode, 'rb') as f:
    # 设置附件的MIME和文件名，这里是jpg类型,可以换png或其他类型:
    mime = MIMEBase('image', 'png', filename='QR.png')
    # 加上必要的头信息:
    mime.add_header('Content-ID', '<0>')
    # 把附件的内容读进来:
    mime.set_payload(qrcode)
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)
    # 登录并发送邮件
    try:
        # 163smtp服务器的端口号为465或
        s = smtplib.SMTP_SSL(mail_host, 465)
        s.set_debuglevel(1)
        s.login(sender, passWord)
        # 给receivers列表中的联系人逐个发送邮件
        for item in receivers:
            msg['To'] = to = item
            s.sendmail(sender, to, msg.as_string())
            # print('Success!')
        s.quit()
        # print("All emails have been sent over!")
    except smtplib.SMTPException as e:
        print("Falied,%s", e)


if __name__ == '__main__':
    send_QR(None, None, './演示.jpg')
