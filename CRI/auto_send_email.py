# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 18:23:28 2020

@author: rmileng
"""
import smtplib
from email.mime.text import MIMEText # 构建邮件正文，可以是text，也可以是HTML
# from email.mime.base import MIMEBase
# from email import encoders
from email.header import Header # 专门构建邮件标题的，这样做，可以支持标题中文
# from email.mime.image import MIMEImage # 为附件中添加图片
from email.mime.multipart import MIMEMultipart  # 构建邮件头信息，包括发件人，接收人，标题等 
from email.mime.application import MIMEApplication  # 构建邮件附件，理论上，只要是文件即可，一般是图片，Excel表格，word文件等
import pandas as pd
import os

def sent_email_from_outlook_text(subject,body,receivers='Lengyueshuang.Luna@outlook.com'):
    
    mail_host='smtp-mail.outlook.com'  #设置服务器
    mail_user='rmileng@nus.edu.sg'    #用户名
    mail_pass='7993725Shuang'   #口令      
     
    sender = 'rmileng@nus.edu.sg'
 #   receivers = ['Lengyueshuang.Luna@outlook.com']      

    message = MIMEText(body, 'plain', 'utf-8') ## body is a string
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = sender
    message['To'] = receivers
#    message['Cc'] = Header(','.join(cc), 'utf-8')   # 抄送
#    message['Bcc'] = Header(','.join(cc), 'utf-8')  # 密送

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

        
def sent_email_from_outlook(subject,body,file_path=[], df=[], receivers='Lengyueshuang.Luna@outlook.com'):

    mail_host='smtp-mail.outlook.com'  #设置服务器
    mail_user='rmileng@nus.edu.sg'    #用户名
    mail_pass='7993725Shuang'   #口令      
     
    sender = 'zengjiajie@nus.edu.sg'
 #   receivers = ['Lengyueshuang.Luna@outlook.com']      
    
    msg = MIMEMultipart('related')
    msg['Subject'] = Header(subject)
    msg["From"] = sender
    msg['To'] = receivers # msg['To'] = ','.join(receiver) for more than one receiver
    
    # text 内容
    content_text = MIMEText(body,'plain', 'utf-8')
    msg.attach(content_text)
    
    # 构造附件
    if len(file_path)==0: # 如果附件存在
        if os.path.isfile(file_path): # 如果附件只有一个文件
            if '\\' in file_path:
                name = file_path.split('\\')[-1]
            else:
                name = file_path.split('/')[-1]
            # 任意类型附件均可
            attach_table = MIMEApplication(open(file_path, 'rb').read())
            # 给附件增加标题(只是把文件名换一下即可，还有附件名称的后缀)
            attach_table.add_header('Content-Disposition', 'attachment',filename=name)
            #  这样的话，附件名称就可以是中文的了，不会出现乱码
            attach_table.set_charset('utf-8')
            msg.attach(attach_table)
    #       只适用于图片类型
    #            fp = open(file_path, 'rb')
    #            images = MIMEImage(fp.read())
    #            fp.close()
    #            images.add_header('Content-ID', name)
    #            msg.attach(images)
        else: # if more than one attachment, ignore situation with subfolder
            subpath = [os.path.join(file_path,l) for l in os.listdir(file_path)]
            for ipath in subpath:
                if '\\' in ipath:
                    name = ipath.split('\\')[-1]
                else:
                    name = ipath.split('//')[-1]
                attach_table = MIMEApplication(open(ipath, 'rb').read())
                attach_table.add_header('Content-Disposition', 'attachment',filename=name)
                attach_table.set_charset('utf-8')
                msg.attach(attach_table)
                
    ## 如果想再正文中展示表格类的内容，最好的方式用HTML
    # html 内容
    pd.set_option('display.max_colwidth', -1)  # 能显示的最大宽度, 否则to_html出来的地址就不全
    if len(df) > 0:
        df_html = df.to_html(escape=False)
        html_msg = get_html_msg(df_html)
    
        content_html = MIMEText(html_msg, "html", "utf-8")
        msg.attach(content_html)
    
    
    try:
        ## Standard process ##
        smtp = smtplib.SMTP(mail_host,587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, receivers, msg.as_string())
        print ("邮件发送成功")
        smtp.quit()
    except Exception as e:
        print(e)


def get_html_msg(df_html):
    """
    1. 构造html信息
    """

    head = \
        """
        <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                    /*居中显示整个表格*/
                    margin: auto;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #105de3;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: Calibri;
                }

                h1 {
                    color: #5db446
                }

                div.header h2 {
                    color: #0002e3;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 28px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 22px;
                    background-color: rgba(0, 2, 227, 0.71);
                    text-shadow: 2px 2px 1px #de4040;
                    color: rgba(239, 241, 234, 0.99);
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    /*width: 60px;*/
                    max-width: 300px;
                    max-height: 300px;
                }

            </STYLE>
        </head>
        """

    # 构造模板的附件（100）
    body = \
        """
        <body>

        <hr>

        <div class="content">
            <!--正文内容-->
            <h2>Table</h2>

            <div>
                <h4></h4>
                {df_html}

            </div>
            <hr>

        </div>
        </body>
        """.format(df_html=df_html)
    html_msg= "<html>" + head + body + "</html>"
    # 这里是将HTML文件输出，作为测试的时候，查看格式用的，正式脚本中可以注释掉
    fout = open('t4.html', 'w', encoding='UTF-8', newline='')
    fout.write(html_msg)
    return html_msg
    