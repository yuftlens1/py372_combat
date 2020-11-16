# -*- coding: UTF-8 -*-
import paramiko,sys,time
spedate = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
filedate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
ipfile = open("d:\\ip.txt",encoding='utf-8')                                                                 #指定IP文件#一组一行
error = open(f'd:\\ssh\\unaccess_{filedate}.csv', 'a')                                                       #错误日志
def ssh_list(iplist):
    passwd = open("d:\\passwd.txt", encoding='utf-8')                                                        #指定密码列表文件#一组一行
    access = open(f'd:\\ssh\\access_{filedate}.csv', 'a')                                                    #成功日志
    while True:
        keylist = (passwd.readline().strip('\n'))
        if len(keylist) < 1:
            return
        try:
            transport = paramiko.Transport(iplist, 22)
            transport.connect(username='root', password=keylist)
            ssh = paramiko.SSHClient()
            ssh._transport = transport
        except Exception as keyerr:
            print(spedate,f"{iprow}\t",keyerr,file=error)
            continue
        else:
            # sftp = paramiko.SFTPClient.from_transport(transport)
            # sftp.get(remotepath='/root/ceph-deploy-ceph.log',localpath='E:/ftp/ceph-deploy-ceph.log')      #下载文件
            # sftp.put(localpath='E:/ftp/test.txt', remotepath='/root/test.txt')                             #上传文件
            # sftp.put(localpath='E:/ftp/ceph-deploy-ceph.log', remotepath='/root/ceph-deploy-ceph.log')     #上传文件
            stdin, stdout, stderr = ssh.exec_command('v1=`cat /etc/redhat-release` && if [ "$v1" = "CentOS Linux release 8.2.2004" ];then echo "匹配,无需升级" ;else echo "不匹配" && mkdir /root/test && echo "升级成功";fi')                   #服务器端执行shell命令
            print(spedate,f"\t{iprow}的密码是{keylist}\t",stdout.read().decode('utf-8'),file=access)
            # print(stderr.read().decode('utf-8'))
            transport.close()
            passwd.close()
            access.close()
            return
while True:
    iprow = (ipfile.readline().strip('\n'))
    if len(iprow) < 1:
        break
    try:
        ssh_list(iprow)
    except Exception as iperr:
        print(spedate,iperr,file=error)
        continue
    else:
        continue
ipfile.close()
error.close()
sys.exit()
# break：跳出所在的当前整个循环，到外层代码继续执行。
# continue：跳出本次循环，从下一个迭代继续运行循环，内层循环执行完毕，外层代码继续运行。
# return：直接返回函数，所有该函数体内的代码（包括循环体）都不会再执行。
# 日志文件按天分割 '%Y-%m-%d'