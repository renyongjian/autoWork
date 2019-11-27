#-*-coding:GBK -*- 
from . import UIManager
import time
import requests
import json


def config(url,phonenumber):
	try:
		showObj = UIManager.showFrame;
		showObj.show_str("正在查找配置文件...\n");
		with open("F:/doc/sipinfo.conf",'r') as configFile:
			data = configFile.read();
		showObj.show_str("正在导入数据...\n");
		json_data = json.loads(data)
		post_data = {};
		showObj.show_str("正在查找号码...\n");
		print_num="号码是:%s\n" %phonenumber;
		showObj.show_str(print_num)
		#for obj in json_data['PhoneNumbers']:
			#if obj['DBID_SIP_PHONE_NUM'] == phonenumber:
				#post_data=obj;
				#showObj.show_str("非常好，号码已经找到...\n");
				#break;
			#else :
				#showObj.show_str("号码还没找到...\n");
		post_data=json_data[phonenumber];
		if post_data:
			showObj.show_str("非常好。。。。。。号码被正常找到\n");
		else:
			showObj.show_str("号码查找失败！！！！\n");
			return False;
		login_data = json_data['LoginData'];
		login_headers = {"User-Agent":"renyongjain"};
		login_url = "http://" + url + "/goform/websLogin";
		refer_url = "http://" + url + "/voip/SIP_Account1.asp?0";
		post_url  = "http://" + url + "/goform/setSip_account";
		refer_headers = {"Referer": refer_url,"User-Agent":"renyongjain"};
		showObj.show_str("正在发起请求...\n");
		ssion = requests.session()
		showObj.show_str("正在登录...\n");
		response = ssion.post(login_url,data=login_data,headers=login_headers)
		showObj.show_str("登录成功，正在修改参数...\n");
		response = ssion.post(post_url,data=post_data,headers=refer_headers)
		showObj.show_str("修改参数完成\n");
	except:
		showObj.show_str("出现异常！！！检查端口或者网络\n");
	finally:
		showObj.show_str("执行结束\n");