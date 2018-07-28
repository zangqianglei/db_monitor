#! /usr/bin/python
# encoding:utf-8

import os
from django.shortcuts import render

from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import StreamingHttpResponse
from django.http import FileResponse


from django.http import HttpResponse
import datetime
from frame import tools
# 配置文件
import ConfigParser
import base64
import frame.models as models_frame
import linux_mon.models as models_linux
import oracle_mon.models as models_oracle
import mysql_mon.models as models_mysql

import easy_check as easy_check
import log_collect as collect
import easy_start as start

# Create your views here.

@login_required(login_url='/login')
def show_all(request):
    # 资产状况统计
    linux_all_cnt = len(models_linux.TabLinuxServers.objects.all())
    linux_seccess_cnt = len(models_linux.LinuxRate.objects.filter(linux_rate_level='success'))
    linux_warning_cnt = len(models_linux.LinuxRate.objects.filter(linux_rate_level='warning'))
    linux_danger_cnt = len(models_linux.LinuxRate.objects.filter(linux_rate_level='danger'))
    ora_all_cnt = len(models_oracle.TabOracleServers.objects.all())
    ora_seccess_cnt = len(models_oracle.OracleDbRate.objects.filter(db_rate_level='success'))
    ora_warning_cnt = len(models_oracle.OracleDbRate.objects.filter(db_rate_level='warning'))
    ora_danger_cnt = len(models_oracle.OracleDbRate.objects.filter(db_rate_level='danger'))
    msql_all_cnt = len(models_mysql.TabMysqlServers.objects.all())
    msql_seccess_cnt = len(models_mysql.MysqlDbRate.objects.filter(db_rate_level='success'))
    msql_warning_cnt = len(models_mysql.MysqlDbRate.objects.filter(db_rate_level='warning'))
    msql_danger_cnt = len(models_mysql.MysqlDbRate.objects.filter(db_rate_level='danger'))
    # 告警
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()

    # top5
    top_5_cpu = models_linux.OsInfo.objects.filter(cpu_used__isnull=False).order_by("-cpu_used")[:5]
    top_5_mem = models_linux.OsInfo.objects.filter(mem_used__isnull=False).order_by("-mem_used")[:5]
    # 当前时间
    now = tools.now()
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')
    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('show_all.html', { 'messageinfo_list': messageinfo_list,'linux_all_cnt':linux_all_cnt,'linux_seccess_cnt':linux_seccess_cnt,'linux_warning_cnt':linux_warning_cnt,'linux_danger_cnt':linux_danger_cnt,'ora_all_cnt':ora_all_cnt,'ora_seccess_cnt':ora_seccess_cnt,'ora_warning_cnt':ora_warning_cnt,'ora_danger_cnt':ora_danger_cnt,
                                                     'msql_all_cnt':msql_all_cnt,'msql_seccess_cnt':msql_seccess_cnt,'msql_warning_cnt':msql_warning_cnt,'msql_danger_cnt':msql_danger_cnt,
                                                   'msg_num': msg_num,'top_5_cpu':top_5_cpu,'top_5_mem':top_5_mem,'now':now,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        msg_num = 0
        msg_last_content = ''
        tim_last = ''
        return render_to_response('show_all.html',
                                  {'messageinfo_list': messageinfo_list, 'linux_all_cnt': linux_all_cnt,
                                   'linux_seccess_cnt': linux_seccess_cnt, 'linux_warning_cnt': linux_warning_cnt,
                                   'linux_danger_cnt': linux_danger_cnt, 'ora_all_cnt': ora_all_cnt,
                                   'ora_seccess_cnt': ora_seccess_cnt, 'ora_warning_cnt': ora_warning_cnt,
                                   'ora_danger_cnt': ora_danger_cnt,
                                   'msql_all_cnt': msql_all_cnt, 'msql_seccess_cnt': msql_seccess_cnt,
                                   'msql_warning_cnt': msql_warning_cnt, 'msql_danger_cnt': msql_danger_cnt,
                                   'msg_num': msg_num, 'top_5_cpu': top_5_cpu, 'top_5_mem': top_5_mem, 'now': now,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})


@login_required(login_url='/login')
def mon_servers(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    # linux监控设备
    linux_servers_list = models_linux.TabLinuxServers.objects.all()
    paginator_linux = Paginator(linux_servers_list, 5)
    page_linux = request.GET.get('page_linux')
    try:
        linuxs_servers = paginator_linux.page(page_linux)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        linuxs_servers = paginator_linux.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        linuxs_servers = paginator_linux.page(paginator_linux.num_pages)
    # Oracle监控设备
    oracle_servers_list = models_oracle.TabOracleServers.objects.all()
    paginator_oracle = Paginator(oracle_servers_list, 5)
    page_oracle = request.GET.get('page_oracle')
    try:
        oracle_servers = paginator_oracle.page(page_oracle)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        oracle_servers = paginator_oracle.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        oracle_servers = paginator_oracle.page(paginator_oracle.num_pages)

    # Mysql监控设备
    mysql_servers_list = models_mysql.TabMysqlServers.objects.all()
    paginator_mysql = Paginator(mysql_servers_list, 5)
    page_mysql = request.GET.get('paginator_mysql')
    try:
        mysql_servers = paginator_mysql.page(page_mysql)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        mysql_servers = paginator_mysql.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        mysql_servers = paginator_mysql.page(paginator_mysql.num_pages)

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('mon_servers.html',
                                  {'linuxs_servers': linuxs_servers,'oracle_servers': oracle_servers,'mysql_servers': mysql_servers, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('mon_servers.html', {'linuxs_servers': linuxs_servers,'oracle_servers': oracle_servers,'mysql_servers': mysql_servers})

@login_required(login_url='/login')
def alarm_setting(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    # 告警策略
    alarm_list = models_frame.TabAlarmConf.objects.all().order_by('db_type')
    paginator_alarm = Paginator(alarm_list, 5)
    page_alarm = request.GET.get('page_alarm')
    try:
        alarm_settings = paginator_alarm.page(page_alarm)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        alarm_settings = paginator_alarm.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        alarm_settings = paginator_alarm.page(paginator_alarm.num_pages)

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('alarm_setting.html',
                                  {'alarm_settings': alarm_settings, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('alarm_setting.html', {'alarm_settings': alarm_settings})


@login_required(login_url='/login')
def alarm_settings_edit(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    rid = request.GET.get('id')
    alarm_setting_edit = models_frame.TabAlarmConf.objects.get(id=rid)
    if request.method == "POST":
        if request.POST.has_key('commit'):
            db_type = request.POST.get('db_type', None)
            alarm_name = request.POST.get('alarm_name', None)

            pct_max = request.POST.get('pct_max', None)
            size_min = request.POST.get('size_min', None)
            time_max = request.POST.get('time_max', None)
            num_max = request.POST.get('num_max', None)

            models_frame.TabAlarmConf.objects.filter(id=rid).update(pct_max = pct_max,
                                                              size_min = size_min, time_max = time_max,num_max = num_max)
            return HttpResponseRedirect('/alarm_settings/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('alarm_settings_edit.html', {'alarm_setting_edit': alarm_setting_edit, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('alarm_settings_edit.html', {'alarm_setting_edit': alarm_setting_edit})


@login_required(login_url='/login')
def linux_servers_edit(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    rid = request.GET.get('id')
    linux_server_edit = models_linux.TabLinuxServers.objects.get(id=rid)
    if request.method == "POST":
        if request.POST.has_key('commit'):
            tags = request.POST.get('tags', None)
            host_name = request.POST.get('host_name', None)
            host = request.POST.get('host', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            connect_cn = request.POST.get('connect', None)
            connect = tools.isno(connect_cn)
            cpu_cn = request.POST.get('cpu', None)
            cpu = tools.isno(cpu_cn)
            mem_cn = request.POST.get('mem', None)
            mem = tools.isno(mem_cn)
            disk_cn = request.POST.get('disk', None)
            disk = tools.isno(disk_cn)
            models_linux.TabLinuxServers.objects.filter(id=rid).update(tags=tags,host_name=host_name, host=host, user=user,
                                                                 password=password, connect_cn=connect_cn,
                                                                 connect=connect,
                                                                 cpu_cn=cpu_cn, cpu=cpu, mem_cn=mem_cn, mem=mem,
                                                                 disk_cn=disk_cn, disk=disk)
            return HttpResponseRedirect('/mon_servers/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('linux_servers_edit.html', {'linux_server_edit': linux_server_edit, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('linux_servers_edit.html', {'linux_server_edit': linux_server_edit})

@login_required(login_url='/login')
def linux_servers_add(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    if request.method == "POST":
        if request.POST.has_key('commit'):
            tags = request.POST.get('tags', None)
            host_name = request.POST.get('host_name', None)
            host = request.POST.get('host', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            connect_cn = request.POST.get('connect', None)
            connect = tools.isno(connect_cn)
            cpu_cn = request.POST.get('cpu', None)
            cpu = tools.isno(cpu_cn)
            mem_cn = request.POST.get('mem', None)
            mem = tools.isno(mem_cn)
            disk_cn = request.POST.get('disk', None)
            disk = tools.isno(disk_cn)
            models_linux.TabLinuxServers.objects.create(tags=tags,host_name=host_name, host=host, user=user, password=password,
                                                  connect_cn=connect_cn, connect=connect,
                                                  cpu_cn=cpu_cn, cpu=cpu, mem_cn=mem_cn, mem=mem, disk_cn=disk_cn,
                                                  disk=disk)
            return HttpResponseRedirect('/mon_servers/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('linux_servers_add.html',
                                  { 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('linux_servers_add.html', )

@login_required(login_url='/login')
def linux_servers_del(request):
    rid = request.GET.get('id')
    models_linux.TabLinuxServers.objects.filter(id=rid).delete()
    return HttpResponseRedirect('/mon_servers/')

@login_required(login_url='/login')
def oracle_servers_add(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    if request.method == "POST":
        if request.POST.has_key('commit'):
            tags = request.POST.get('tags', None)
            host = request.POST.get('host', None)
            port = request.POST.get('port', None)
            service_name = request.POST.get('service_name', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            user_os = request.POST.get('user_os', None)
            password_os = base64.encodestring(request.POST.get('password_os', None))
            connect_cn = request.POST.get('connect', None)
            connect = tools.isno(connect_cn)
            tbs_cn = request.POST.get('tbs', None)
            tbs = tools.isno(tbs_cn)
            adg_cn = request.POST.get('adg', None)
            adg = tools.isno(adg_cn)
            temp_tbs_cn = request.POST.get('temp_tbs', None)
            temp_tbs = tools.isno(temp_tbs_cn)
            undo_tbs_cn = request.POST.get('undo_tbs', None)
            undo_tbs = tools.isno(undo_tbs_cn)
            conn_cn = request.POST.get('conn', None)
            conn = tools.isno(conn_cn)
            err_info_cn = request.POST.get('err_info', None)
            err_info = tools.isno(err_info_cn)
            invalid_index_cn = request.POST.get('invalid_index', None)
            invalid_index = tools.isno(invalid_index_cn)
            oracle_lock_cn = request.POST.get('oracle_lock', None)
            oracle_lock = tools.isno(oracle_lock_cn)
            oracle_pwd_cn = request.POST.get('oracle_pwd', None)
            oracle_pwd = tools.isno(oracle_pwd_cn)
            oracle_pga_cn = request.POST.get('oracle_pga', None)
            oracle_pga = tools.isno(oracle_pga_cn)
            oracle_archive_cn = request.POST.get('oracle_archive', None)
            oracle_archive = tools.isno(oracle_archive_cn)
            models_oracle.TabOracleServers.objects.create(tags=tags,host=host, port=port, service_name=service_name,
                                                   user=user, password=password,
                                                   user_os=user_os, password_os=password_os, connect=connect,
                                                   connect_cn=connect_cn, tbs=tbs, tbs_cn=tbs_cn,
                                                   adg=adg, adg_cn=adg_cn, temp_tbs=temp_tbs, temp_tbs_cn=temp_tbs_cn,
                                                   undo_tbs=undo_tbs, undo_tbs_cn=undo_tbs_cn,
                                                   conn=conn, conn_cn=conn_cn, err_info=err_info,
                                                   err_info_cn=err_info_cn,invalid_index=invalid_index,invalid_index_cn=invalid_index_cn,
                                                          oracle_lock =oracle_lock,oracle_lock_cn=oracle_lock_cn,oracle_pwd =oracle_pwd,oracle_pwd_cn=oracle_pwd_cn,pga=oracle_pga,pga_cn=oracle_pga_cn,archive=oracle_archive,archive_cn=oracle_archive_cn)
            return HttpResponseRedirect('/mon_servers/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('oracle_servers_add.html',
                                  { 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('oracle_servers_add.html', )

@login_required(login_url='/login')
def oracle_servers_del(request):
    rid = request.GET.get('id')
    models_oracle.TabOracleServers.objects.filter(id=rid).delete()
    return HttpResponseRedirect('/mon_servers/')

@login_required(login_url='/login')
def oracle_servers_edit(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    rid = request.GET.get('id')
    oracle_server_edit = models_oracle.TabOracleServers.objects.get(id=rid)
    if request.method == "POST":
        if request.POST.has_key('commit'):
            tags = request.POST.get('tags', None)
            host = request.POST.get('host', None)
            port = request.POST.get('port', None)
            service_name = request.POST.get('service_name', None)
            user = request.POST.get('user', None)
            password = request.POST.get('password', None)
            password_value = models_oracle.TabOracleServers.objects.values("password").filter(id=rid)[0]
            if  password.encode('utf-8') + '\n'  != password_value['password'].encode('utf-8'):
                password = base64.encodestring(request.POST.get('password', None))
            user_os = request.POST.get('user_os', None)
            password_os = request.POST.get('password_os', None)
            password_os_value =  models_oracle.TabOracleServers.objects.values("password_os").filter(id=rid)[0]
            if  password_os.encode('utf-8') + '\n'  != password_os_value['password_os'].encode('utf-8'):
                password_os = base64.encodestring(request.POST.get('password_os', None))
            connect_cn = request.POST.get('connect', None)
            connect = tools.isno(connect_cn)
            tbs_cn = request.POST.get('tbs', None)
            tbs = tools.isno(tbs_cn)
            adg_cn = request.POST.get('adg', None)
            adg = tools.isno(adg_cn)
            temp_tbs_cn = request.POST.get('temp_tbs', None)
            temp_tbs = tools.isno(temp_tbs_cn)
            undo_tbs_cn = request.POST.get('undo_tbs', None)
            undo_tbs = tools.isno(undo_tbs_cn)
            conn_cn = request.POST.get('conn', None)
            conn = tools.isno(conn_cn)
            err_info_cn = request.POST.get('err_info', None)
            err_info = tools.isno(err_info_cn)
            invalid_index_cn = request.POST.get('invalid_index', None)
            invalid_index = tools.isno(invalid_index_cn)
            oracle_lock_cn = request.POST.get('oracle_lock', None)
            oracle_lock = tools.isno(oracle_lock_cn)
            oracle_pwd_cn = request.POST.get('oracle_pwd', None)
            oracle_pwd = tools.isno(oracle_pwd_cn)
            oracle_pga_cn = request.POST.get('oracle_pga', None)
            oracle_pga = tools.isno(oracle_pga_cn)
            oracle_archive_cn = request.POST.get('oracle_archive', None)
            oracle_archive = tools.isno(oracle_archive_cn)
            models_oracle.TabOracleServers.objects.filter(id=rid).update(tags=tags,host=host, port=port, service_name=service_name,
                                                                  user=user, password=password,
                                                                  user_os=user_os, password_os=password_os,
                                                                  connect=connect,
                                                                  connect_cn=connect_cn, tbs=tbs, tbs_cn=tbs_cn,
                                                                  adg=adg, adg_cn=adg_cn, temp_tbs=temp_tbs,
                                                                  temp_tbs_cn=temp_tbs_cn,
                                                                  undo_tbs=undo_tbs, undo_tbs_cn=undo_tbs_cn,
                                                                  conn=conn, conn_cn=conn_cn, err_info=err_info,
                                                                  err_info_cn=err_info_cn,invalid_index=invalid_index,invalid_index_cn=invalid_index_cn,
                                                          oracle_lock =oracle_lock,oracle_lock_cn=oracle_lock_cn,oracle_pwd =oracle_pwd,oracle_pwd_cn=oracle_pwd_cn,pga=oracle_pga,pga_cn=oracle_pga_cn,archive=oracle_archive,archive_cn=oracle_archive_cn)
            return HttpResponseRedirect('/mon_servers/')

        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')


    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('oracle_servers_edit.html', {'oracle_server_edit': oracle_server_edit,'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('oracle_servers_edit.html',{'oracle_server_edit': oracle_server_edit})

@login_required(login_url='/login')
def mysql_servers_add(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    if request.method == "POST":
        if request.POST.has_key('commit'):
            tags = request.POST.get('tags', None)
            host = request.POST.get('host', None)
            port = request.POST.get('port', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            user_os = request.POST.get('user_os', None)
            password_os = base64.encodestring(request.POST.get('password_os', None))
            connect_cn = request.POST.get('connect', None)
            connect = tools.isno(connect_cn)
            repl_cn = request.POST.get('repl', None)
            repl = tools.isno(repl_cn)
            conn_cn = request.POST.get('conn', None)
            conn = tools.isno(conn_cn)
            err_info_cn = request.POST.get('err_info', None)
            err_info = tools.isno(err_info_cn)
            models_mysql.TabMysqlServers.objects.create(host=host, port=port, tags=tags,
                                                   user=user, password=password,
                                                   user_os=user_os, password_os=password_os, connect=connect,
                                                   connect_cn=connect_cn,
                                                   repl=repl, repl_cn=repl_cn,
                                                   conn=conn, conn_cn=conn_cn, err_info=err_info,
                                                   err_info_cn=err_info_cn)
            return HttpResponseRedirect('/mon_servers/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('mysql_servers_add.html',
                                  { 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('mysql_servers_add.html', )

@login_required(login_url='/login')
def mysql_servers_del(request):
    rid = request.GET.get('id')
    models_mysql.TabMysqlServers.objects.filter(id=rid).delete()
    return HttpResponseRedirect('/mon_servers/')

@login_required(login_url='/login')
def mysql_servers_edit(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    rid = request.GET.get('id')
    mysql_server_edit = models_mysql.TabMysqlServers.objects.get(id=rid)
    if request.method == "POST":
        if request.POST.has_key('commit'):
            tags = request.POST.get('tags', None)
            host = request.POST.get('host', None)
            port = request.POST.get('port', None)
            user = request.POST.get('user', None)
            password = request.POST.get('password', None)
            password_value = models_mysql.TabMysqlServers.objects.values("password").filter(id=rid)[0]
            if password.encode('utf-8') + '\n' != password_value['password'].encode('utf-8'):
                password = base64.encodestring(request.POST.get('password', None))
            user_os = request.POST.get('user_os', None)
            password_os = request.POST.get('password_os', None)
            password_os_value = models_mysql.TabMysqlServers.objects.values("password_os").filter(id=rid)[0]
            if password_os.encode('utf-8') + '\n' != password_os_value['password_os'].encode('utf-8'):
                password_os = base64.encodestring(request.POST.get('password_os', None))
            connect_cn = request.POST.get('connect', None)
            connect = tools.isno(connect_cn)
            repl_cn = request.POST.get('repl', None)
            repl = tools.isno(repl_cn)
            conn_cn = request.POST.get('conn', None)
            conn = tools.isno(conn_cn)
            err_info_cn = request.POST.get('err_info', None)
            err_info = tools.isno(err_info_cn)
            models_mysql.TabMysqlServers.objects.filter(id=rid).update(tags=tags,host=host, port=port,
                                                                  user=user, password=password,
                                                                  user_os=user_os, password_os=password_os,
                                                                  connect=connect,
                                                                  connect_cn=connect_cn,
                                                                  repl=repl, repl_cn=repl_cn,
                                                                  conn=conn, conn_cn=conn_cn, err_info=err_info,
                                                                  err_info_cn=err_info_cn)
            return HttpResponseRedirect('/mon_servers/')

        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')


    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('mysql_servers_edit.html', {'mysql_server_edit': mysql_server_edit,'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('mysql_servers_edit.html',{'mysql_servers_edit': mysql_server_edit})

@login_required(login_url='/login')
def show_alarm(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    paginator_msg = Paginator(messageinfo_list, 5)
    page_msg = request.GET.get('page')
    try:
        messageinfos = paginator_msg.page(page_msg)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        messageinfos = paginator_msg.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messageinfos = paginator_msg.page(paginator_msg.num_pages)

    if request.POST.has_key('logout'):
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('show_alarm.html', {'messageinfos': messageinfos, 'msg_num': msg_num,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        msg_num = 0

        return render_to_response('show_alarm.html', {'messageinfo_list': messageinfo_list,'msg_num': msg_num})

@login_required(login_url='/login')
def recorder(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')
    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_list})

@login_required(login_url='/login')
def recorder_db(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    recorder_db_list = models_frame.EventRecorder.objects.filter(event_section='数据库').order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_db_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_db_list})

@login_required(login_url='/login')
def recorder_os(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    recorder_os_list = models_frame.EventRecorder.objects.filter(event_section='系统').order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_os_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_os_list})

@login_required(login_url='/login')
def recorder_others(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    recorder_others_list = models_frame.EventRecorder.objects.filter(event_section='其他').order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_others_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_others_list})

@login_required(login_url='/login')
def recorder_err(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    recorder_err_list = models_frame.EventRecorder.objects.filter(event_type='故障').order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_err_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_err_list})

@login_required(login_url='/login')
def recorder_chg(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    recorder_chg_list = models_frame.EventRecorder.objects.filter(event_type='变更').order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_chg_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_chg_list})

@login_required(login_url='/login')
def recorder_upd(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('-record_time')
    recorder_upd_list = models_frame.EventRecorder.objects.filter(event_type='升级').order_by('-record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('recorder.html',
                                  {'recorder_list': recorder_upd_list,'all_nums':all_nums,'sys_nums':sys_nums,'db_nums':db_nums,'other_nums':other_nums,
                                   'err_nums':err_nums,'chg_nums':chg_nums,'upg_nums':upg_nums, 'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder.html', {'recorder_list': recorder_upd_list})

@login_required(login_url='/login')
def recorder_del(request):
    rid = request.GET.get('id')
    models_frame.EventRecorder.objects.filter(id=rid).delete()
    return HttpResponseRedirect('/recorder/')


@login_required(login_url='/login')
def recorder_add(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    recorder_list = models_frame.EventRecorder.objects.order_by('record_time')
    all_nums = len(recorder_list)
    sys_nums =  len(models_frame.EventRecorder.objects.filter(event_section='系统'))
    db_nums =  len(models_frame.EventRecorder.objects.filter(event_section='数据库'))
    other_nums =  len(models_frame.EventRecorder.objects.filter(event_section='其他'))
    err_nums =  len(models_frame.EventRecorder.objects.filter(event_type='故障'))
    chg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='变更'))
    upg_nums =  len(models_frame.EventRecorder.objects.filter(event_type='升级'))
    if request.method == "POST":
        if request.POST.has_key('commit'):
            event_section = request.POST.get('event_section', None)
            event_type = request.POST.get('event_type', None)
            if event_type == unicode('升级', 'utf-8'):
                event_type_color = 'success'
            elif event_type == unicode('变更', 'utf-8'):
                event_type_color = 'warning'
            else:
                event_type_color = 'danger'
            event_content = request.POST.get('event_content', None)
            models_frame.EventRecorder.objects.create(event_section=event_section, event_type=event_type,
                                                event_type_color=event_type_color, event_content=event_content)
            return HttpResponseRedirect('/recorder/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')


    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        if request.method == 'POST':
            logout(request)
            return HttpResponseRedirect('/login/')
        return render_to_response('recorder_add.html',
                                  {'recorder_list': recorder_list, 'all_nums': all_nums, 'sys_nums': sys_nums,
                                   'db_nums': db_nums, 'other_nums': other_nums,
                                   'err_nums': err_nums, 'chg_nums': chg_nums, 'upg_nums': upg_nums,
                                   'messageinfo_list': messageinfo_list,
                                   'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('recorder_add.html', {'recorder_list': recorder_list})



@login_required(login_url='/login')
def sys_setting(request):
    # 读配置文件
    conf = ConfigParser.ConfigParser()
    conf_path = os.getcwd() + '/check_alarm/config/db_monitor.conf'
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    now = tools.now()
    conf.read(conf_path)
    # 告警邮件
    sender = conf.get("email", "sender")
    smtpserver = conf.get("email", "smtpserver")
    username = conf.get("email", "username")
    password_email = conf.get("email", "password")
    receiver = conf.get("email", "receiver")
    msg_from = conf.get("email", "msg_from")
    # 采集周期
    check_sleep_time = conf.get("policy", "check_sleep_time")
    alarm_sleep_time = conf.get("policy", "alarm_sleep_time")
    next_send_email_time = conf.get("policy", "next_send_email_time")
   # 监控数据存放
    host = conf.get("target_mysql", "host")
    port = conf.get("target_mysql", "port")
    user = conf.get("target_mysql", "user")
    password_mysql = conf.get("target_mysql", "password")
    dbname = conf.get("target_mysql", "dbname")

    if request.method == 'POST':
        # 修改邮箱设置
        if request.POST.has_key('commit_email'):
            sender = request.POST.get('sender', None)
            smtpserver = request.POST.get('smtpserver', None)
            username = request.POST.get('username', None)
            password_email = request.POST.get('password_email', None)
            receiver = request.POST.get('receiver', None)
            msg_from = request.POST.get('msg_from', None)
            conf.set("email","sender",sender)
            conf.set("email", "smtpserver", smtpserver)
            conf.set("email", "username", username)
            conf.set("email", "password_email", password_email)
            conf.set("email", "receiver", receiver)
            conf.set("email", "msg_from", msg_from)
            check_box = request.REQUEST.get('check_box')
            if check_box:
                conf.set("email", "is_send", '1')
            else:
                conf.set("email", "is_send", '0')
            conf.write(open(conf_path, "w"))
            return HttpResponseRedirect('/sys_setting/')
        # 修改采集周期设置
        elif request.POST.has_key('commit_check'):
            check_sleep_time = request.POST.get('check_sleep_time', None)
            alarm_sleep_time = request.POST.get('alarm_sleep_time', None)
            next_send_email_time = request.POST.get('next_send_email_time', None)
            conf.set("policy", "check_sleep_time", check_sleep_time)
            conf.set("policy", "alarm_sleep_time", alarm_sleep_time)
            conf.set("policy", "next_send_email_time", next_send_email_time)
            conf.write(open(conf_path, "w"))
            return HttpResponseRedirect('/sys_setting/')
        # 修改数据库设置
        elif request.POST.has_key('commit_db'):
            host = request.POST.get('host', None)
            port = request.POST.get('port', None)
            user = request.POST.get('user', None)
            password_mysql = request.POST.get('password_mysql', None)
            dbname = request.POST.get('dbname', None)
            conf.set("target_mysql", "host", host)
            conf.set("target_mysql", "user", user)
            conf.set("target_mysql", "port", port)
            conf.set("target_mysql", "password", password_mysql)
            conf.set("target_mysql", "dbname", dbname)
            conf.write(open(conf_path, "w"))
            return HttpResponseRedirect('/sys_setting/')

        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('sys_setting.html',
                                  {'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last,
                                   'sender': sender,'smtpserver':smtpserver,'username':username,
                                   'password_email': password_email,'receiver':receiver,'msg_from':msg_from,
                                   'check_sleep_time':check_sleep_time,'alarm_sleep_time':alarm_sleep_time,
                                   'next_send_email_time':next_send_email_time,'host':host,'port':port,'user':user,
                                   'password_mysql': password_mysql,'dbname':dbname,'now':now})
    else:
        return render_to_response('sys_setting.html', {'messageinfo_list': messageinfo_list,
                                   'sender': sender,'smtpserver':smtpserver,'username':username,
                                   'password_email': password_email,'receiver':receiver,'msg_from':msg_from,
                                   'check_sleep_time':check_sleep_time,'alarm_sleep_time':alarm_sleep_time,
                                   'next_send_email_time':next_send_email_time,'host':host,'port':port,'user':user,
                                   'password_mysql': password_mysql,'dbname':dbname,'now':now} )

@login_required(login_url='/login')
def my_check(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    select_type = request.GET.get('select_type')
    if not select_type:
        select_type = 'Oracle数据库'.decode("utf-8")
    date_range = request.GET.get('date_range')
    if not date_range:
        date_range = '1天'.decode("utf-8")
    select_tags = request.GET.get('select_tags')
    if not select_tags:
        select_tags = '选择一个或多个'.decode("utf-8")
    select_form = request.GET.get('select_form')
    if not select_form:
        select_form = 'excel'
    file_tag = request.GET.get('file_tag')
    if not file_tag:
        file_tag = ''
    check_err = models_frame.CheckInfo.objects.filter(check_tag=file_tag)
    begin_time = request.GET.get('begin_time')
    if not begin_time:
        begin_time = ''
    end_time = request.GET.get('end_time')
    if not end_time:
        end_time = ''

    # 当前时间
    now = tools.now()
    if request.method == 'POST':
        if request.POST.has_key('go_check'):
            select_type = request.POST.get('select_type', None)
            date_range = request.POST.get('date_range', None)
            select_tags = request.POST.getlist('select_tags', None)
            select_form = request.POST.get('select_form', None)
            # begin_time = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
            begin_time = tools.range(date_range)
            end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_tag = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            check_file_name  = 'oracheck_' + file_tag +  '.xls'
            easy_check.ora_check(select_tags,begin_time,end_time,check_file_name,file_tag)
            tags = ''
            for tag in select_tags:
                tags =  tag + ','
            return HttpResponseRedirect('/my_check?select_type=%s&date_range=%s&select_tags=%s&select_form=%s&file_tag=%s&begin_time=%s&end_time=%s' %(select_type,date_range,tags,select_form,file_tag,begin_time,end_time))

        else:
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('my_check.html', { 'messageinfo_list': messageinfo_list,'msg_num':msg_num,'now':now,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last,
                                                     'select_type':select_type,'date_range':date_range,'select_tags':select_tags,'select_form':select_form,'file_tag':file_tag,'check_err':check_err,'begin_time':begin_time,'end_time':end_time})
    else:
        msg_num = 0
        msg_last_content = ''
        tim_last = ''
        return render_to_response('my_check.html',
                                  {'messageinfo_list': messageinfo_list,'now': now,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last,
                                   'select_type': select_type, 'date_range': date_range, 'select_tags': select_tags,
                                   'select_form': select_form,'file_tag':file_tag,'check_err':check_err,'begin_time':begin_time,'end_time':end_time})


def page_not_found(request):
    return render(request, '404.html')


def download(request):
    select_form = request.GET.get('select_form')
    file_tag = request.GET.get('file_tag')
    file_path = os.getcwd() + '\check_result' + '\\'
    if select_form == 'excel':
        if not file_tag:
            file = file_path + 'oracheck.xls'
            file_name = 'oracheck.xls'
        else:
            file = file_path + 'oracheck_' + file_tag + '.xls'
            file_name = 'oracheck_' + file_tag + '.xls'
    elif select_form == 'txt':
        if not file_tag:
            file = file_path + 'oracheck.txt'
            file_name = 'oracheck.txt'
        else:
            file = file_path + 'oracheck_' + file_tag + '.txt'
            file_name = 'oracheck_' + file_tag + '.txt'

    file=open(file,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename=%s' %file_name
    return response

@login_required(login_url='/login')
def my_tools(request):
    # 告警
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()

    now = tools.now()
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')
    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('my_tools.html', { 'messageinfo_list': messageinfo_list,
                                                   'msg_num': msg_num,'now':now,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        msg_num = 0
        msg_last_content = ''
        tim_last = ''
        return render_to_response('my_tools.html',
                                  {'messageinfo_list': messageinfo_list, 'now': now,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})

@login_required(login_url='/login')
def log_collect(request):
    # 告警
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()

    # 日志采集列表
    log_collect_list = models_frame.LogCollectConf.objects.all()
    paginator_log = Paginator(log_collect_list, 5)
    page_log = request.GET.get('page_log')
    try:
        log_collects = paginator_log.page(page_log)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        log_collects = paginator_log.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        log_collects = paginator_log.page(paginator_log.num_pages)
    now = tools.now()
    if request.method == 'POST':
        if request.POST.has_key('go_collect'):
            log_type = '日志采集'
            local_dir = request.POST.get('local_dir', None)
            collect.go_collect(local_dir)
            return HttpResponseRedirect('/log_info?log_type=%s' %log_type)

        else:
            logout(request)
            return HttpResponseRedirect('/login/')
    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('log_collect.html', { 'messageinfo_list': messageinfo_list,'log_collects':log_collects,
                                                   'msg_num': msg_num,'now':now,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        msg_num = 0
        msg_last_content = ''
        tim_last = ''
        return render_to_response('log_collect.html',
                                  {'messageinfo_list': messageinfo_list, 'log_collects':log_collects,'now': now,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})

@login_required(login_url='/login')
def log_collects_edit(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    rid = request.GET.get('id')
    log_collect_edit = models_frame.LogCollectConf.objects.get(id=rid)
    if request.method == "POST":
        if request.POST.has_key('commit'):
            app_name = request.POST.get('app_name', None)
            host = request.POST.get('host', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            log_name = request.POST.get('log_name', None)
            log_path = request.POST.get('log_path', None)
            models_frame.LogCollectConf.objects.filter(id=rid).update(app_name=app_name,host=host, user=user,
                                                                 password=password, log_name = log_name,
                                                                 log_path = log_path)
            return HttpResponseRedirect('/log_collect/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('log_collects_edit.html', {'log_collect_edit': log_collect_edit, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('log_collects_edit.html', {'log_collect_edit': log_collect_edit})

@login_required(login_url='/login')
def log_collects_add(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    if request.method == "POST":
        if request.POST.has_key('commit'):
            app_name = request.POST.get('app_name', None)
            host = request.POST.get('host', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            log_name = request.POST.get('log_name', None)
            log_path = request.POST.get('log_path', None)
            models_frame.LogCollectConf.objects.create(app_name=app_name,host=host, user=user, password=password,
                                                       log_name=log_name, log_path=log_path)
            return HttpResponseRedirect('/log_collect/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('log_collects_add.html',
                                  { 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('log_collects_add.html', )

@login_required(login_url='/login')
def log_collects_del(request):
    rid = request.GET.get('id')
    models_frame.LogCollectConf.objects.filter(id=rid).delete()
    return HttpResponseRedirect('/log_collect/')

@login_required(login_url='/login')
def easy_start(request):
    # 告警
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()

    # 程序启停列表
    easy_start_list = models_frame.EasyStartConf.objects.all()
    paginator_start = Paginator(easy_start_list, 5)
    page_start = request.GET.get('page_start')
    try:
        easy_starts = paginator_start.page(page_start)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        easy_starts = paginator_start.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        easy_starts = paginator_start.page(paginator_start.num_pages)
    now = tools.now()
    if request.method == 'POST':
        if request.POST.has_key('go_start'):
            log_type = '程序启停'
            start.go_start()
            return HttpResponseRedirect('/log_info?log_type=%s' % log_type)
            return HttpResponseRedirect('/log_collects_info')
        elif request.POST.has_key('reset'):
            upd_1_sql = "update easy_start_conf set process_check_result=''"
            upd_2_sql = "update easy_start_conf set check_log_result=''"
            tools.mysql_exec(upd_1_sql,'')
            tools.mysql_exec(upd_2_sql,'')
            return HttpResponseRedirect('/easy_start/')

        else:
            logout(request)
            return HttpResponseRedirect('/login/')
    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('easy_start.html', { 'messageinfo_list': messageinfo_list,'easy_starts':easy_starts,
                                                   'msg_num': msg_num,'now':now,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        msg_num = 0
        msg_last_content = ''
        tim_last = ''
        return render_to_response('easy_start.html',
                                  {'messageinfo_list': messageinfo_list, 'easy_starts':easy_starts,'now': now,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})

@login_required(login_url='/login')
def easy_starts_edit(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    rid = request.GET.get('id')
    easy_start_edit = models_frame.EasyStartConf.objects.get(id=rid)
    if request.method == "POST":
        if request.POST.has_key('commit'):
            oper_type = request.POST.get('oper_type', None)
            app_name = request.POST.get('app_name', None)
            host = request.POST.get('host', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            name = request.POST.get('name', None)
            do_cmd = request.POST.get('do_cmd', None)
            process_check = request.POST.get('process_check', None)
            check_log = request.POST.get('check_log', None)
            models_frame.EasyStartConf.objects.filter(id=rid).update(oper_type=oper_type,app_name=app_name,host=host, user=user,
                                                                 password=password,name=name, do_cmd = do_cmd,process_check = process_check,
                                                                     check_log = check_log)
            return HttpResponseRedirect('/easy_start/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('easy_starts_edit.html', {'easy_start_edit': easy_start_edit, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('easy_starts_edit.html', {'easy_start_edit': easy_start_edit})

@login_required(login_url='/login')
def easy_starts_add(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    if request.method == "POST":
        if request.POST.has_key('commit'):
            oper_type = request.POST.get('oper_type', None)
            app_name = request.POST.get('app_name', None)
            host = request.POST.get('host', None)
            user = request.POST.get('user', None)
            password = base64.encodestring(request.POST.get('password', None))
            name = request.POST.get('name', None)
            do_cmd = request.POST.get('do_cmd', None)
            process_check = request.POST.get('process_check', None)
            check_log = request.POST.get('check_log', None)
            models_frame.EasyStartConf.objects.create(oper_type=oper_type,app_name=app_name,host=host, user=user,
                                                                 password=password, do_cmd = do_cmd, name = name,process_check = process_check,
                                                                     check_log = check_log)
            return HttpResponseRedirect('/easy_start/')
        elif request.POST.has_key('logout'):
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('easy_starts_add.html',
                                  { 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('easy_starts_add.html', )

@login_required(login_url='/login')
def easy_starts_del(request):
    rid = request.GET.get('id')
    models_frame.EasyStartConf.objects.filter(id=rid).delete()
    return HttpResponseRedirect('/easy_start/')


@login_required(login_url='/login')
def log_info(request):
    # 告警
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    log_type = request.GET.get('log_type')

    # 日志采集列表
    log_info = models_frame.ManyLogs.objects.filter(log_type=log_type)
    paginator_log = Paginator(log_info, 10)
    page_log = request.GET.get('page_log')
    try:
        logs = paginator_log.page(page_log)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator_log.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator_log.page(paginator_log.num_pages)
    now = tools.now()

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('log_info.html', {'messageinfo_list': messageinfo_list, 'logs':logs,
                                                   'msg_num': msg_num,'now':now,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        msg_num = 0
        msg_last_content = ''
        tim_last = ''
        return render_to_response('log_info.html',
                                  {'messageinfo_list': messageinfo_list, 'logs':logs,'now': now,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})