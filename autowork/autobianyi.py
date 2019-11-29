#-*-coding:GBK -*- 
import os
import sys
import subprocess
import paramiko
import time
import json


from . import UIManager
from . import interactive

class svnClient:
	def __init__(self):
		self.svn_path="D:/test";
		if not os.path.exists(self.svn_path):
			print('svn工作路径：%s 不存在，退出程序' % self.svn_path)
			exit()
	
	def get_svn_path(self):
		return self.svn_path;
	
	def set_svn_path(self,input_path):
		self.svn_path = input_path;
	def svn_update(self):
		args = 'cd /d ' + self.svn_path + ' & svn update';
		with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
			output = proc.communicate();
			print('执行svn update命令输出：%s' % str(output));
			if not output[1]:
				print("svn update 执行成功");
				return True;
			else:
				print("svn update 执行失败");
				return False;
	def svn_commit(self,ver_num,path):
		commit_line='svn commit -m "修改版本号到%s" %s' %(ver_num,path);
		print(commit_line)
		args = 'cd /d ' + self.svn_path + ' & ' + commit_line;
		with subprocess.Popen(args, shell=True, universal_newlines = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
			output = proc.communicate();
			print('执行svn commit命令输出：%s' % str(output));
			if not output[1]:
				print("svn commit 执行成功");
				return True;
			else:
				print("svn commit 执行失败");
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
		
	def recv(self,bytes):
		return self.channel.recv(bytes);
		
	def close(self):
		self.channel.close()
		self.trans.close()
		#print(stderr.read());
		

def auto_bianyi(path):
	data="";
	with open("F:/doc/ssh_login.conf") as file:
		data=file.read();
	json_data=json.loads(data);
	host=json_data['host'];
	password=json_data['pass'];
	user=json_data['user'];
	port=json_data['port'];
	cmd1=json_data['cmd1'];
	cmd2=json_data['cmd2'];
	
	ssh = sshClient(host=host,port=(int)(port),user=user,password=password);
	time.sleep(0.5);
	res = ssh.recv(1024);
	sys.stdout.write(res.decode())
	sys.stdout.flush()
	time.sleep(0.5);
	ssh.sendCmd(cmd1);
	time.sleep(0.5);
	res=ssh.recv(1024);
	sys.stdout.write(res.decode())
	sys.stdout.flush()
	time.sleep(0.5);
	ssh.sendCmd(cmd2);
	time.sleep(0.5);
	res=ssh.recv(1024);
	time.sleep(0.5);
	#maybe need input password
	input_pass="%s\n" %password
	ssh.sendCmd(input_pass);
	#wait
	time.sleep(20);
	ssh.close();
	
	#svn_client=svnClient();
	#svn_client.set_svn_path(path);
	#os.chdir(path);
	#svn_client.svn_update();
	#svn_client.svn_commit("1.2","test.txt");