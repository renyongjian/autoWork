#-*-coding:utf-8 -*- 

import smtplib
import json
from email.mime.text import MIMEText
from email.header import Header
from . import UIManager

# 第三方 SMTP 服务
mail_host=""; #设置服务器
mail_user="";   #用户名
mail_pass="";  #口令 


sender = "";
receivers = [];# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
json_data = {};



message = MIMEText('autowork', 'plain', 'utf-8')
message['From'] = Header("renyongjian", 'utf-8')
message['To'] =  Header("renyongjian", 'utf-8')

subject = 'auto work'
message['Subject'] = Header(subject, 'utf-8')


def send_mail():
	try:
		smtpObj = smtplib.SMTP(); 
		showObj=UIManager.showFrame;
		with open("F:/doc/mailinfo.conf",'r') as configFile:
			data = configFile.read();
			showObj.show_str("正在导入数据...\n");
			json_data = json.loads(data);
			showObj.show_str("导入数据成功...\n");
		mail_host=json_data['mail_host'];
		mail_user=json_data['mail_user'];
		mail_pass=json_data['mail_pass'];
		receivers = [json_data['receivers']];
		sender=json_data['sender'];
		showObj.show_str("正在连接....\n");
		smtpObj.connect(mail_host, 25);    # 25 为 SMTP 端口号
		showObj.show_str("连接成功，正在登陆...\n");
		smtpObj.login(mail_user,mail_pass)  
		showObj.show_str("登陆成功，正在发送邮件...\n");
		smtpObj.sendmail(sender, receivers, message.as_string())
		showObj.show_str("成功发送\n");
	except smtplib.SMTPException:
		showObj.show_str("发送失败!!\n");