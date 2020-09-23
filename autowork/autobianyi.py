#-*-coding:GBK -*- 
import os
import sys
import subprocess
import paramiko
import time
import json
import select
import shutil



from . import UIManager
from . import mysendmail

class svnClient:
	def __init__(self):
		self.svn_path="D:/test";
		if not os.path.exists(self.svn_path):
			print('svn����·����%s �����ڣ��˳�����' % self.svn_path)
			exit()
	
	def get_svn_path(self):
		return self.svn_path;
	
	def set_svn_path(self,input_path):
		self.svn_path = input_path;
	def svn_update(self):
		args = 'cd /d ' + self.svn_path + ' & svn update';
		with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
			output = proc.communicate();
			print('ִ��svn update���������%s' % str(output));
			if not output[1]:
				print("svn update ִ�гɹ�");
				return True;
			else:
				print("svn update ִ��ʧ��");
				return False;
	def svn_get_version(self):
		args = 'cd /d ' + self.svn_path + ' & svn info';
		with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
			output = proc.communicate();
			#print('ִ��svn update���������%s' % str(output));
			if not output[1]:
				print("svn get version ִ�гɹ�");
				out_str=str(output);
				print(out_str);
				list=out_str.split('\\n');
				print(list)
				for line in list:
					if "Revision:" in line :
						version_list= line.split(':');
						print(version_list[1]);
						return version_list[1].replace(' ','');
			else:
				print("svn get version ִ��ʧ��");
				return False;
				
	def svn_commit(self,ver_num,path):
		commit_line='svn commit -m "�Զ����룬�޸İ汾�ŵ�%s" %s' %(ver_num,path);
		print(commit_line)
		args = 'cd /d ' + self.svn_path + ' & ' + commit_line;
		with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
			output = proc.communicate();
			print('ִ��svn commit���������%s' % str(output));
			if not output[1]:
				print("svn commit ִ�гɹ�");
				return True;
			else:
				print("svn commit ִ��ʧ��");
				return False;
	

class sshClient:
	def __init__(self,host,port,user,password):
		self.trans = paramiko.Transport((host, port));
		self.trans.start_client();
		self.trans.auth_password(username=user, password=password);
		self.channel = self.trans.open_session();
		self.channel.get_pty();
		self.channel.invoke_shell();
		
	def sendCmd(self,cmd):
		self.channel.sendall(cmd);
		
	def recv(self,timeout):
		data=b'';
		while True:
			try:
				readable,w,e= select.select([self.channel],[],[],timeout);
				if self.channel in readable:
					data = self.channel.recv(1024);
					sys.stdout.write(data.decode())
					sys.stdout.flush()
				else:
					return data.decode();
			except TimeoutError:
				return data;
		
	def close(self):
		self.channel.close()
		self.trans.close()
		#print(stderr.read());
		
def delete_dire(dire):
	dir_list = []
	for root, dirs, files in os.walk(dire):
		for afile in files:
			os.remove(os.path.join(root, afile))
		for adir in dirs:
			dir_list.append(os.path.join(root, adir))
	for bdir in dir_list:
		os.rmdir(bdir)
		
def debug(str_data):
	data = "%s\n" %str_data;
	showObj = UIManager.showFrame;
	showObj.show_str(data);
	
def auto_bianyi(product,versions):
	data="";
	path="";
	sw_version_name="sw_version=";
	new_versions= versions.split(',');
	
	
	debug(new_versions)

	#login to svn .
	svn_client=svnClient();
	
	#change config file 
	#get config files 
	for sw_version in new_versions:
		debug("sw version is %s" %sw_version);
		debug("���ڵ��������ļ�...");
		with open("F:/doc/bianyi.conf",'r') as byconfig:
			byconfig_data=byconfig.read();
		json_data=json.loads(byconfig_data);
		debug("���������ļ��ɹ�");
		debug("��������svnĿ¼...");
		path=json_data[product]['svn_dir'];
		svn_client.set_svn_path(path);
		debug("���ڽ���svnĿ¼...");
		os.chdir(path);
		debug("���ڸ���svnĿ¼...");
		svn_client.svn_update();
		debug("�����޸������ļ�...");
		#�޸������ļ�
		if(json_data):
			for tmp_file in json_data[product]['files']:#�ҵ�����Ҫ�޸ĵ������ļ���
				#change config file
				i=0;
				found = False;
				with open(tmp_file,'r') as fp:
					fp_data = fp.readlines();
					for line in fp_data:
						if(sw_version_name in line):
							line=line.replace('\n','');
							#�����+num����ʾ�Ӽ���ֵ����˼��һ����+1
							if "+" in sw_version:
								add_num=int(sw_version[-1:]);
								cur_version = line[-3:];
								cur_version_num = int(cur_version[-1:])+int(cur_version[-3:-2])*10;
								cur_version_num += add_num;
								sw_version = str(int(cur_version_num/10))+"."+ str(cur_version_num%10);
								debug("new version is after add is %s" %sw_version);
							#�����same����ʾ��ʹ�õ�ǰ�İ汾�ţ������á�
							if sw_version == "same" or sw_version == "" or sw_version == " ":
								debug("����Ҫ�޸������ļ�");
								sw_version=line[-3:];
							if(line[-3:] != sw_version):
								line=line.replace(' ','');
								fp_data[i]=line[:-3]+sw_version + '\n';
								debug("�Ѿ��ҵ������޸��˰汾�š���");
							found =True;
							break;
						i+=1;
					if(found):
						with open(tmp_file,'w') as fp_write:
							fp_write.writelines(fp_data);
		else:
			break;
		debug("�޸������ļ����");
		#�Զ��ύ��svn
		svn_client.svn_commit(sw_version,path);
		debug("�����ύ��svn...");
		#��ȡsvn�İ汾�ţ���������
		debug("���ڸ���svn�����һ�ȡ���µİ汾��...");
		svn_client.svn_update();
		svn_version = svn_client.svn_get_version();
		debug("���µ�svn_version �� %s" %svn_version);
		
		debug("���ڵ�½��������...");
		#��¼�����������Զ�ִ�����е�����
		host = json_data['login']['host'];
		password = json_data['login']['pass'];
		user = json_data['login']['user'];
		port = json_data['login']['port'];
		cmds = json_data[product]['cmds'];
		flag_dir = json_data[product]['flag_dir'];
		ssh = sshClient(host=host,port=(int)(port),user=user,password=password);
		for cmd in cmds:
			recv_data = "";
			debug("����ִ������:%s" %cmd);
			ssh.sendCmd(cmd);
			recv_data = ssh.recv(10);
			if "password for" in recv_data:
				debug("��Ҫ��������...");
				input_pass="%s\n" %password
				debug("����������� %s" %input_pass);
				ssh.sendCmd(input_pass);
			if "build_fw" in cmd:
				if " fw" in cmd:
					debug("�ٴθ���svn�����һ�ȡ���µİ汾��...");
					svn_client.svn_update();
					svn_version = svn_client.svn_get_version();
					debug("���µ�svn_version �� %s" %svn_version);
				while True:
					recv_data = ssh.recv(10);
					if flag_dir in recv_data:
						break;
		debug("����ִ�����...");
		#����ִ����ϣ������ϣ�Ҫ�Ķ����Ѿ����ˣ�������취������ϣ���ĵط�
		debug("���ڿ�����Ҫ�Ķ���...");
		image_dir = json_data[product]['image_dir'];
		linux_tmp_dir=json_data[product]['linux_tmp_dir'];
		tmp_dir=json_data[product]['tmp_dir'];
		#����Ŀ��Ŀ¼����ʼ����
		cmd = "cd %s\n" %(image_dir);
		ssh.sendCmd(cmd);
		recv_data = ssh.recv(1);
		cmd = "cp DailyFw_r%s\t\t\t  %s -rf\n" %(svn_version,linux_tmp_dir);
		ssh.sendCmd(cmd);
		recv_data = ssh.recv(1);
		ssh.close();
		
		debug("���ڿ�����Ҫ�Ķ�����ָ����windowsĿ¼...");
		#get fws by version,send images
		fw_dir=json_data[product]['fw_dir']+sw_version;
		#delete_dire(fw_dir);
		shutil.rmtree(fw_dir,True);
		try :
			debug("���ڴ� %s ������ %s"  %(tmp_dir,fw_dir));
			shutil.copytree(tmp_dir,fw_dir);
			debug("�����ɹ�");
			mysendmail.send_mail("�ɹ����Զ����� %s %s ���" %(product,sw_version));
		except:
			debug("����ʧ��");
			mysendmail.send_mail("ʧ�ܣ��Զ����� %s %s ����" %(product,sw_version));
		
		debug("ִ�����")
		
		
		