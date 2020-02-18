import paramiko
import json

class ParamikoComando():
    #try:
    #    with open('/home/pi/raspberryremote/src/localhost.json') as file:
    #        data = json.load(file)
    #        HOST = data['hostname']
    #except:
    #    HOST = ''
    HOST = ''
    USERNAME = ''
    PASSWORD = ''
    def __init__(self):
        self.client = paramiko.SSHClient()

        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def conectar(self):
        self.client.connect(self.HOST, username=self.USERNAME, password=self.PASSWORD)

    def ejecutarcomando(self,comando,pty):
        #ruta = '/home/mrthc/paramiko7/'
        ruta = '/home/pi/indoor/'
        stdin ,stdout ,stderr = self.client.exec_command('echo  ' +self.PASSWORD +' | sudo -E python3  ' +ruta+comando, get_pty=pty)
        return stdin,stdout,stderr

    def pid(self,comando):
        proceso = " | sudo -S ps aux|grep "+comando+" |grep -v grep |awk '{print $2}'"
        stdin, stdout, stderr = self.client.exec_command('echo  ' + ParamikoComando.PASSWORD + proceso)
        pid = stdout.readlines()
        print(pid)
        #pid = pid[0].strip('\n')
        return pid

    def matar(self,pid):
        kill = " | sudo -S kill -9 "
        stdin, stdout, stderr = self.client.exec_command('echo  ' + ParamikoComando.PASSWORD + kill + pid)

    def matarsig(self,pid):
        kill = " | sudo -S kill "
        stdin, stdout, stderr = self.client.exec_command('echo  ' + ParamikoComando.PASSWORD + kill + pid)
