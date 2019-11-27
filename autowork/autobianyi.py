#-*-coding:GBK -*- 
import os
import subprocess

from . import UIManager


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
	
	
def auto_bianyi(path):
	svn_client=svnClient();
	svn_client.set_svn_path(path);
	os.chdir(path);
	#svn_client.svn_update();
	svn_client.svn_commit("1.2","test.txt");