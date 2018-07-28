#! /usr/bin/python
# encoding:utf-8


from django.conf.urls import patterns, include, url
# 导入对应app的views文件
from frame import views as frame
from linux_mon import views as linux_mon
from oracle_mon import views as oracle_mon
from mysql_mon import views as mysql_mon
from login import views as login
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'time_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^linux_monitor/', linux_mon.linux_monitor),
    (r'^oracle_monitor/', oracle_mon.oracle_monitor),
    (r'^mysql_monitor/', mysql_mon.mysql_monitor),
    (r'^show_oracle/', oracle_mon.show_oracle),
    (r'^show_mysql/', mysql_mon.show_mysql),
    (r'^show_mysql_repl/', mysql_mon.show_mysql_repl),
    (r'^begin/', frame.show_all),
    (r'^my_check/', frame.my_check),
    (r'^show_linux_rate/', linux_mon.show_linux_rate),
    (r'^show_oracle_rate/', oracle_mon.show_oracle_rate),
    (r'^show_mysql_rate/', mysql_mon.show_mysql_rate),
    (r'^show_alarm/', frame.show_alarm),
    (r'^show_linux/$', linux_mon.show_linux),
    (r'^show_oracle_resource/', oracle_mon.show_oracle_resource),
    (r'^mon_servers/', frame.mon_servers),
    (r'^alarm_settings/', frame.alarm_setting),
    (r'^alarm_settings_edit$', frame.alarm_settings_edit),
    (r'^linux_servers_add/', frame.linux_servers_add),
    (r'^linux_servers_edit$', frame.linux_servers_edit),
    (r'^linux_servers_del$', frame.linux_servers_del),
    (r'^oracle_servers_add/', frame.oracle_servers_add),
    (r'^oracle_servers_edit$', frame.oracle_servers_edit),
    (r'^oracle_servers_del$', frame.oracle_servers_del),
    (r'^mysql_servers_add/', frame.mysql_servers_add),
    (r'^mysql_servers_edit$', frame.mysql_servers_edit),
    (r'^mysql_servers_del$', frame.mysql_servers_del),
    (r'^recorder/', frame.recorder),
    (r'^login/$', login.login_in),
    (r'^login$', login.login_in),
    (r'^recorder_add', frame.recorder_add),
    (r'^recorder_db', frame.recorder_db),
    (r'^recorder_os', frame.recorder_os),
    (r'^recorder_others', frame.recorder_others),
    (r'^recorder_err', frame.recorder_err),
    (r'^recorder_chg', frame.recorder_chg),
    (r'^recorder_upd', frame.recorder_upd),
    (r'^recorder_del$', frame.recorder_del),
    (r'^sys_setting/', frame.sys_setting),
    (r'^download$', frame.download),
    (r'^my_tools/', frame.my_tools),
    (r'^log_collect/', frame.log_collect),
    (r'^log_collects_edit$', frame.log_collects_edit),
    (r'^log_collects_del$', frame.log_collects_del),
    (r'^log_collects_add/', frame.log_collects_add),
    (r'^log_info$', frame.log_info),
    (r'^easy_start/', frame.easy_start),
    (r'^easy_starts_edit$', frame.easy_starts_edit),
    (r'^easy_starts_del$', frame.easy_starts_del),
    (r'^easy_starts_add/', frame.easy_starts_add),
     url(r'^admin/', include(admin.site.urls)),
)

handler404 = frame.page_not_found