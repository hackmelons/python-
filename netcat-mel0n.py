import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd),
                                    stderr=subprocess.STDOUT)
    return output.decode()

class NetMel0n:
    def __init__(self,args,buffer = None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
   
    def send(self):
        self.socket.connect((self.args.target,self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        
        try:
            while True:
                recv_len =1
                response = ''
                while recv_len:
                    data = self.socket.recv(8192)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 8192:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('成功暂停')
            self.socket.close()
            sys.exit()
            
    def listen(self):
        self.socket.bind((self.args.target,self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target = self.handle,args=(client_socket,)
            )
            client_thread.start()

    def handle(self,client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(1024)
                if data:
                   file_buffer += data
                else:
                   break
            
            with open(self.args.upload ,'wb') as f:
                f.write(file_buffer_)
            message = f'Save file {self.args.upload}'
            client_socket.send(message.encode())
        
        elif self.args.commmand:    #这里不知道为什么command实际运行的时候报错，得用commmand
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'XLSEC: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f' server killed {e}')
                    self.socket.close()
                    sys.exit()
        
        
if __name__ =='__main__':
    parser = argparse.ArgumentParser(
        description='玄鸾安全-mel0n',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
            netmel0n.py -t 127.0.0.1 -p 1212 -l -c                       # 在127.0.0.1的1212端口创建一个交互式的命令行shell
            netmel0n.py -t 127.0.0.1 -p 1212 -l -u=文件.txt               #上传文件.txt到127.0.0.1的1212端口
            netmel0n.py -t 127.0.0.1 -p 1212 -l -e=\"cat /etc/passwd\"   #在127.0.0.1的1212端口执行cat /etc/passwd 命令
            echo 'XLSEC HACKERS'| ./netmel0n.py -t 127.0.0.1 -p 1212     #把内容输入到127.0.0.1的1212端口
            netmel0n.py -t 127.0.0.1 -p 1212                             #连接到127.0.0.1的1212端口
        '''))
    parser.add_argument('-c','--commmand',action='store_true',help = '命令行')
    parser.add_argument('-l','--listen',action= 'store_true',help = '启动监听')
    parser.add_argument('-e','--execute',help = '后面加上执行的命令')
    parser.add_argument('-t','--target',default = '127.0.0.1', help = '目标IP地址')
    parser.add_argument('-p','--port',type = int ,default=1212,help = '指定端口')
    parser.add_argument('-u','--upload',help = '后面跟上要上传的文件')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
        
    nc = NetMel0n(args, buffer.encode())
    nc.run()
    