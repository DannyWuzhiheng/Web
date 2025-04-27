import random as rd
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email(*args):
    msg = MIMEText(args[0], 'html', 'utf-8')
    msg['From'] = args[1]
    msg['To'] = args[4]
    msg['Subject'] = args[-1]
    try:
        server = smtplib.SMTP_SSL(args[2])
        server.login(args[1], args[3])
        server.sendmail(args[1], args[-2], msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPAuthenticationError as e:
        print(f"认证失败: {e}，请检查邮箱账号和授权码。")
    except Exception as e:
        print(f"发送邮件时出现错误: {e}")
    finally:
        if 'server' in locals():
            server.quit()


mesg = str(rd.randint(100000, 999999))
send_mailaddres = "noreply_kscixbirds@163.com"
send_mailserver = "smtp.163.com"
code = "EDkMkCf4WWHiZEdu"
to_email = input("收件邮箱: ")
subject = "KSCIX 邮箱验证码"

# 调用发送邮件函数
mail_list = [mesg, send_mailaddres, send_mailserver, code, to_email, subject]
send_email(*mail_list)