#! /usr/bin/python
# encoding:utf-8

import MySQLdb
import cx_Oracle
import datetime,time
import ConfigParser
import os
import paramiko



host_mysql ='192.168.48.50'
user_mysql = 'root'
password_mysql = 'mysqld'
port_mysql = 3306
dbname = 'db_monitor'

# 操作监控数据存放目标库(mysql)
def mysql_exec(sql,val):
    try:
    	conn=MySQLdb.connect(host=host_mysql,user=user_mysql,passwd=password_mysql,port=int(port_mysql),connect_timeout=5,charset='utf8')
    	conn.select_db(dbname)
    	curs = conn.cursor()
    	if val <> '':
            curs.execute(sql,val)
        else:
            curs.execute(sql)
        conn.commit()
        curs.close()
        conn.close()
    except Exception,e:
       print "mysql execute: " + str(e)


def mysql_query(sql):
    conn=MySQLdb.connect(host=host_mysql,user=user_mysql,passwd=password_mysql,port=int(port_mysql),connect_timeout=5,charset='utf8')
    conn.select_db(dbname)
    cursor = conn.cursor()
    count=cursor.execute(sql)
    if count == 0 :
        result=0
    else:
        result=cursor.fetchall()
    return result
    cursor.close()
    conn.close()



def now():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def isno(p):
    if p == unicode('是','utf-8'):
        return 1
    else:
        return 0

def test_orc(host,port,service_name,user,password):
    url = host + ':' + port + '/' + service_name
    try:
        conn = cx_Oracle.connect(user, password, url)
        cur = conn.cursor()
        cur.execute("select 1 from dual")
        result = 1
        result_msg = 'connect success!'
    except Exception,e:
        result = 0
        error_msg = "%s 数据库连接失败：%s" % (url, unicode(str(e), errors='ignore'))

def ora_qry(url,username,password,sql):
    conn = cx_Oracle.connect(username, password, url)
    cur = conn.cursor()
    cur.execute(sql)
    title = [i[0] for i in cur.description]
    g = lambda k: "%-8s" % k
    title = map(g,title)
    result = cur.fetchall()
    for i in title:
        print i,
    return result

def range(range_value):
    if range_value == unicode('1小时', 'utf-8'):
        cpu_range = 1
        begin_time = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    elif range_value== unicode('0.5小时', 'utf-8'):
        cpu_range = 0.5
        begin_time = (datetime.datetime.now() - datetime.timedelta(hours=0.5)).strftime("%Y-%m-%d %H:%M:%S")
    elif range_value == unicode('1天', 'utf-8'):
        cpu_range = 0.5
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    elif range_value == unicode('7天', 'utf-8'):
        cpu_range = 0.5
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    elif range_value == unicode('30天', 'utf-8'):
        cpu_range = 0.5
        begin_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    return begin_time

def my_log(log_type,log_info,err_info):
    insert_sql = "insert into many_logs(log_type,log_info,err_info) values(%s,%s,%s)"
    value = (log_type, log_info,err_info)
    mysql_exec(insert_sql, value)
