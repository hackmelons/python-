import socket

target_host = "127.0.0.1"
target_port = 9997

#创建socket项目,SOCK_DGRAM表示无保障的数据报套接字，它是一种无连接服务
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#发送一些数据
client.sendto(b"AAABBBCCC",(target_host,target_port))

#接受一些数据
data, addr = client.recvfrom(1024)

print(data.decode())
client.close()