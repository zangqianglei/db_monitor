#! /usr/bin/python
# encoding:utf-8

import paramiko
import os
import time
import base64
import tools as tools

# 执行命令,
def exec_command(host,user,password,command):
    list = []
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, 22, user, password)
        std_in, std_out, std_err = ssh_client.exec_command(command)
        for line in std_out:
            list.append(line.strip("\n"))
        ssh_client.close()
        return list
    except Exception, e:
        print e

# 上传文件
def sftp_upload_file(host,user,password,server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception, e:
        print e

def sftp_upload_dir(host,user,password,remote_dir,local_dir):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        for root,dirs,files in os.walk(local_dir):
            print root,dirs,files
            # remote_path = remote_dir + '/' + dirs
            for filespatch in files:
                local_file = os.path.join(root,filespatch)
                a = local_file.replace(local_dir,'')
                remote_file = remote_dir +'/' + local_file.replace("\\", "/")
                sftp.put(local_file, remote_file)
                print '成功上传：%s 到 %s' %(local_file,remote_file)

    except Exception,e:
        print e



def oracle_install(host,user,password):
    log_type = 'Oracle部署'
    tools.mysql_exec("delete from many_logs where log_type = 'Oracle部署'",'')
    # 清除目标目录
    cmd = 'rm -rf /tmp/oracle_install'
    exec_command(host, user, password, cmd)
    # 创建文件目录
    cmd = 'mkdir -p /tmp/oracle_install/oracle_rpms/centos6'
    exec_command(host, user, password, cmd)
    # 上传安装部署文件
    sftp_upload_dir(host,user,password,'/tmp','oracle_install')

    #1. 安装rpm包
    cmd = 'sh /tmp/oracle_install/1_ora_yum.sh > /tmp/oracle_install/1_ora_yum.log'
    exec_command(host, user, password, cmd)
    #2.环境初始化，建组、用户，配置资源限制，内核参数
    cmd = 'sh /tmp/oracle_install/2_ora_init.sh > /tmp/oracle_install/2_ora_init.log'
    exec_command(host, user, password, cmd)
    #3. 创建目录
    cmd = 'sh /tmp/oracle_install/3_fd_init.sh > /tmp/oracle_install/3_fd_init.log'
    exec_command(host, user, password, cmd)


if __name__ == '__main__':
    host = '192.168.48.50'
    user = 'root'
    password = 'mysqld'
    oracle_install(host,user,password)










