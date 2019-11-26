#-*-coding:GBK -*- 
import logging
import telnetlib
import time


class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()

    # �˺���ʵ��telnet��¼����
    def login_host(self,host_ip,username,password):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip,port=23)
        except:
            logging.warning('%s��������ʧ��'%host_ip)
            return False
        # �ȴ�login���ֺ������û��������ȴ�10��
        self.tn.read_until(b'login: ',timeout=10)
        self.tn.write(username.encode('ascii') + b'\n')
        # �ȴ�Password���ֺ������û��������ȴ�10��
        self.tn.read_until(b'Password: ',timeout=10)
        self.tn.write(password.encode('ascii') + b'\n')
        # ��ʱ��������ȡ���ؽ������������㹻��Ӧʱ��
        time.sleep(2)
        # ��ȡ��¼���
        # read_very_eager()��ȡ�����ǵ����ϴλ�ȡ֮�󱾴λ�ȡ֮ǰ���������
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logging.warning('%s��¼�ɹ�'%host_ip)
            return True
        else:
            logging.warning('%s��¼ʧ�ܣ��û������������'%host_ip)
            return False

    # �˺���ʵ��ִ�д�����������������ִ�н��
    def execute_some_command(self,command):
        # ִ������
        self.tn.write(command.encode('ascii')+b'\n')
        time.sleep(2)
        # ��ȡ������
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.warning('����ִ�н����\n%s' % command_result)

    # �˳�telnet
    def logout_host(self):
        self.tn.write(b"exit\n")

def auto_telnet_change_ip():
    host_ip1 = '192.168.2.52';
    host_ip2 = '192.168.2.58';
    username = 'admin';
    password = '123';
    command1 = 'ifconfig eth2.1 192.168.2.58 up';
    command2 = 'ifconfig eth2.1 192.168.2.52 up';
    telnet_client = TelnetClient()
    # �����¼�������True����ִ�����Ȼ���˳�
    while True:
        if telnet_client.login_host(host_ip1,username,password):
            telnet_client.execute_some_command(command1)
            telnet_client.logout_host()
        elif telnet_client.login_host(host_ip2,username,password):
            telnet_client.execute_some_command(command2)
            telnet_client.logout_host() 
            time.sleep(5);