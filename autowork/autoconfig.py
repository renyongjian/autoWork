#-*-coding:GBK -*- 
from . import UIManager
import time
import requests
import json


def config(url,phonenumber):
	try:
		showObj = UIManager.showFrame;
		showObj.show_str("���ڲ��������ļ�...\n");
		with open("F:/doc/sipinfo.conf",'r') as configFile:
			data = configFile.read();
		showObj.show_str("���ڵ�������...\n");
		json_data = json.loads(data)
		post_data = {};
		showObj.show_str("���ڲ��Һ���...\n");
		print_num="������:%s\n" %phonenumber;
		showObj.show_str(print_num)
		#for obj in json_data['PhoneNumbers']:
			#if obj['DBID_SIP_PHONE_NUM'] == phonenumber:
				#post_data=obj;
				#showObj.show_str("�ǳ��ã������Ѿ��ҵ�...\n");
				#break;
			#else :
				#showObj.show_str("���뻹û�ҵ�...\n");
		post_data=json_data[phonenumber];
		if post_data:
			showObj.show_str("�ǳ��á��������������뱻�����ҵ�\n");
		else:
			showObj.show_str("�������ʧ�ܣ�������\n");
			return False;
		login_data = json_data['LoginData'];
		login_headers = {"User-Agent":"renyongjain"};
		login_url = "http://" + url + "/goform/websLogin";
		refer_url = "http://" + url + "/voip/SIP_Account1.asp?0";
		post_url  = "http://" + url + "/goform/setSip_account";
		refer_headers = {"Referer": refer_url,"User-Agent":"renyongjain"};
		showObj.show_str("���ڷ�������...\n");
		ssion = requests.session()
		showObj.show_str("���ڵ�¼...\n");
		response = ssion.post(login_url,data=login_data,headers=login_headers)
		showObj.show_str("��¼�ɹ��������޸Ĳ���...\n");
		response = ssion.post(post_url,data=post_data,headers=refer_headers)
		showObj.show_str("�޸Ĳ������\n");
	except:
		showObj.show_str("�����쳣���������˿ڻ�������\n");
	finally:
		showObj.show_str("ִ�н���\n");