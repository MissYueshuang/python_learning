# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:43:32 2020

@author: e0431396
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header
## add attachment
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
 
# 第三方 SMTP 服务
mail_host='smtp-mail.outlook.com'  #设置服务器
mail_user='rmileng@nus.edu.sg'    #用户名
mail_pass='7993725Shuang'   #口令 
 
 
sender = 'rmileng@nus.edu.sg'
receivers = ['Lengyueshuang.Luna@outlook.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

message = MIMEMultipart('mixed') #总的内容

# 邮件内容
message.attach(MIMEText('你好, 麻烦开通防火墙, 详情见附件~ 谢谢 ！！', 'plain', 'utf-8'))

# 邮件主题 
subject = '申请开通防火墙'
message['Subject'] = Header(subject, 'utf-8')

# 附件相关(csv)
part = MIMEBase('application', "octet-stream") # standard, just remember
part.set_payload(open(r"D:\LYS\python_learning\web_scraping\myexercise\douban_movie250\douban_movie.csv", "rb").read(),'utf-8')
encoders.encode_base64(part)
# filename 不要省略了文件名的后缀 否则会变成乱码 eg.:ATT00002.bin
part.add_header('Content-Disposition', 'attachment', filename="douban_movie.csv") 
message.attach(part)

## 插入图片
fp = open(r'D:\LYS\python_learning\web_scraping\json-python-convert.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()
message.attach(msgImage)

## 发送邮件
try:
    ## Standard process ##
    smtp = smtplib.SMTP(mail_host,587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(mail_user, mail_pass)
    smtp.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
    smtp.quit()
except Exception as e:
    print(e)


# aggereate into a function (without attachment) !!!!!!!!!!!!!
def sent_email_from_outlook(subject,body):
    mail_host='smtp-mail.outlook.com'  #设置服务器
    mail_user='rmileng@nus.edu.sg'    #用户名
    mail_pass='7993725Shuang'   #口令      
     
    sender = 'rmileng@nus.edu.sg'
    receivers = ['Lengyueshuang.Luna@outlook.com']      

    message = MIMEText(body, 'plain', 'utf-8') ## body is a string
    message['Subject'] = Header(subject, 'utf-8')

    try:
        ## Standard process ##
        smtp = smtplib.SMTP(mail_host,587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
        smtp.quit()
    except Exception as e:
        print(e)
    
sent_email_from_outlook('flight info','机票降价了，快去买！')  