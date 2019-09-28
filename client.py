'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/8/10 9:45
@Software: PyCharm
@File    : client.py
'''
"""
name:Levi
chatroom client
"""
from socket import *
import sys,os
import signal

#子进程发送消息
def do_child(s,name,addr):
    while True:
        text = input("发言(输入quit退出):")
        #用户退出
        if text == "quit":
            msg = "Q" + name
            s.sendto(msg.encode(),addr)
            #从子进程中杀掉父进程
            os.kill(os.getppid(),signal.SIGKILL)
            sys.exit("退出聊天室")
        else:
            msg = "C %s %s"%(name,text)
            s.sendto(msg.encode(),addr)

#父进程接受消息
def do_parent(s):
    while True:
        msg,addr = s.recvfrom(1024)
        print(msg.decode() + "\n发言(输入quit退出):",end='')

def main():
    Host = "127.0.0.1"
    Port = 8888
    Addr = (Host,Port)

    sockfd = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input("请输入姓名：")
        msg = "L " + name
        sockfd.sendto(msg.encode(),Addr)
        data,addr = sockfd.recvfrom(1024)
        if data.decode() == 'OK':
            print("@进入聊天室@")
            break
        else:
            print(data.decode())

    # 创建一级子进程
    pid1 = os.fork()
    if pid1 < 0:
        print("创建一级子进程失败")
    elif pid1 == 0:
        do_child(sockfd,name,Addr)
    else:
        do_parent(sockfd)

if __name__ == '__main__':
    main()