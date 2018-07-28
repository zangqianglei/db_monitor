#! /usr/bin/python
# encoding:utf-8

from django.shortcuts import render

from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
import datetime
from frame import tools
# 配置文件
import ConfigParser
import base64
import frame.models as models_frame
import oracle_mon.models as models_oracle

# Create your views here.


@login_required(login_url='/login')
def oracle_monitor(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    tagsinfo = models_oracle.TabOracleServers.objects.all().order_by('tags')

    tagsdefault = request.GET.get('tagsdefault')
    if not tagsdefault:
        tagsdefault = models_oracle.TabOracleServers.objects.order_by('tags')[0].tags

    conn_range_default = request.GET.get('conn_range_default')
    if not conn_range_default:
        conn_range_default = '1小时'.decode("utf-8")

    undo_range_default = request.GET.get('undo_range_default')
    if not undo_range_default:
        undo_range_default = '1小时'.decode("utf-8")

    tmp_range_default = request.GET.get('tmp_range_default')
    if not tmp_range_default:
        tmp_range_default = '1小时'.decode("utf-8")

    conn_begin_time = tools.range(conn_range_default)
    undo_begin_time = tools.range(undo_range_default)
    tmp_begin_time = tools.range(tmp_range_default)

    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        oracleinfo = models_oracle.OracleDb.objects.get(tags=tagsdefault)
    except models_oracle.OracleDb.DoesNotExist:
        oracleinfo = models_oracle.OracleDbHis.objects.filter(tags=tagsdefault,percent_process__isnull=False).order_by('-chk_time')[0]

    eventinfo = models_oracle.OracleDbEvent.objects.filter(tags=tagsdefault)
    lockinfo = models_oracle.OracleLock.objects.filter(tags=tagsdefault)

    try:
        conninfo = models_oracle.OracleDb.objects.get(tags=tagsdefault)
    except models_oracle.OracleDb.DoesNotExist:
        conninfo =  models_oracle.OracleDbHis.objects.filter(tags=tagsdefault, percent_process__isnull=False).order_by('-chk_time')[0]

    conngrow = models_oracle.OracleDbHis.objects.filter(tags=tagsdefault, percent_process__isnull=False).filter(
        chk_time__gt=conn_begin_time, chk_time__lt=end_time).order_by('-chk_time')
    conngrow_list = list(conngrow)
    conngrow_list.reverse()

    try:
        undoinfo = models_oracle.OracleUndoTbs.objects.get(tags=tagsdefault)
    except models_oracle.OracleUndoTbs.DoesNotExist:
        undoinfo =  models_oracle.OracleUndoTbsHis.objects.filter(tags=tagsdefault, pct_used__isnull=False).order_by('-chk_time')[0]

    undogrow = models_oracle.OracleUndoTbsHis.objects.filter(tags=tagsdefault, pct_used__isnull=False).filter(
        chk_time__gt=undo_begin_time, chk_time__lt=end_time).order_by('-chk_time')
    undogrow_list = list(undogrow)
    undogrow_list.reverse()

    try:
        tmpinfo = models_oracle.OracleTmpTbs.objects.get(tags=tagsdefault,tmp_tbs_name='TEMP')
    except models_oracle.OracleTmpTbs.DoesNotExist:
        tmpinfo =  models_oracle.OracleTmpTbsHis.objects.filter(tags=tagsdefault, pct_used__isnull=False).order_by('-chk_time')[0]

    tmpgrow = models_oracle.OracleTmpTbsHis.objects.filter(tags=tagsdefault, pct_used__isnull=False).filter(
        chk_time__gt=tmp_begin_time, chk_time__lt=end_time).order_by('-chk_time')
    tmpgrow_list = list(tmpgrow)
    tmpgrow_list.reverse()

    if request.method == 'POST':
        if request.POST.has_key('select_tags') or request.POST.has_key('select_conn') or request.POST.has_key('select_undo') or request.POST.has_key('select_tmp'):
            if request.POST.has_key('select_tags'):
                tagsdefault = request.POST.get('select_tags', None).encode("utf-8")
            elif request.POST.has_key('select_conn'):
                conn_range_default = request.POST.get('select_conn',None)
            elif request.POST.has_key('select_undo'):
                undo_range_default = request.POST.get('select_undo', None)
            elif request.POST.has_key('select_tmp'):
                tmp_range_default = request.POST.get('select_tmp', None)
            return HttpResponseRedirect('/oracle_monitor?tagsdefault=%s&conn_range_default=%s&undo_range_default=%s&tmp_range_default=%s' %(tagsdefault,conn_range_default,undo_range_default,tmp_range_default))

        else:
            logout(request)
            return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('oracle_monitor.html', {'conngrow_list':conngrow_list,'undogrow_list': undogrow_list,'tmpinfo':tmpinfo,'tmpgrow_list':tmpgrow_list, 'tagsdefault':tagsdefault, 'tagsinfo':tagsinfo, 'oracleinfo': oracleinfo,'undoinfo': undoinfo,'eventinfo':eventinfo,'lockinfo':lockinfo, 'messageinfo_list': messageinfo_list,
                                                   'msg_num': msg_num,'conn_range_default':conn_range_default,'undo_range_default':undo_range_default,'tmp_range_default':tmp_range_default,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('oracle_monitor.html', {'conngrow_list':conngrow_list,'undogrow_list': undogrow_list, 'tagsdefault':tagsdefault, 'tagsinfo':tagsinfo, 'tmpinfo':tmpinfo,'tmpgrow_list':tmpgrow_list,'oracleinfo': oracleinfo,'undoinfo': undoinfo,
                                                          'eventinfo':eventinfo,'lockinfo':lockinfo,'conn_range_default':conn_range_default,'undo_range_default':undo_range_default,'tmp_range_default':tmp_range_default})


@login_required(login_url='/login')
def show_oracle(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    dbinfo_list = models_oracle.OracleDb.objects.all()
    paginator = Paginator(dbinfo_list, 10)
    page = request.GET.get('page')
    try:
        dbinfos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        dbinfos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        dbinfos = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('show_oracle.html',
                                  {'dbinfos': dbinfos, 'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('show_oracle.html', {'dbinfos': dbinfos})


@login_required(login_url='/login')
def show_oracle_resource(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    dbinfo_list = models_oracle.OracleDb.objects.all()
    tbsinfo_list = models_oracle.OracleTbs.objects.order_by('-pct_used')
    # 分页
    paginator_tbs = Paginator(tbsinfo_list, 5)
    undotbsinfo_list = models_oracle.OracleUndoTbs.objects.order_by('-pct_used')
    paginator_undo = Paginator(undotbsinfo_list, 5)
    tmptbsinfo_list = models_oracle.OracleTmpTbs.objects.order_by('-pct_used')
    paginator_tmp = Paginator(tmptbsinfo_list, 5)

    page_tbs = request.GET.get('page_tbs')
    try:
        tbsinfos = paginator_tbs.page(page_tbs)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tbsinfos = paginator_tbs.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tbsinfos = paginator_tbs.page(paginator_tbs.num_pages)
    page_undo = request.GET.get('page_undo')
    try:
        undotbsinfos = paginator_undo.page(page_undo)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        undotbsinfos = paginator_undo.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        undotbsinfos = paginator_undo.page(paginator_undo.num_pages)
    page_tmp = request.GET.get('page_tmp')
    try:
        tmptbsinfos = paginator_undo.page(page_tmp)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tmptbsinfos = paginator_tmp.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tmptbsinfos = paginator_tmp.page(paginator_tmp.num_pages)

    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('show_oracle_resource.html',
                                  {'tbsinfos': tbsinfos, 'undotbsinfos':undotbsinfos,'tmptbsinfos':tmptbsinfos,'messageinfo_list': messageinfo_list, 'msg_num': msg_num,
                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('show_oracle_resource.html', { 'tbsinfos': tbsinfos, 'undotbsinfos':undotbsinfos, 'tmptbsinfos':tmptbsinfos})


@login_required(login_url='/login')
def show_oracle_rate(request):
    messageinfo_list = models_frame.TabAlarmInfo.objects.all()
    oracle_rate_list = models_oracle.OracleDbRate.objects.order_by("db_rate")
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')
    if messageinfo_list:
        msg_num = len(messageinfo_list)
        msg_last = models_frame.TabAlarmInfo.objects.latest('id')
        msg_last_content = msg_last.alarm_content
        tim_last = (datetime.datetime.now() - msg_last.alarm_time).seconds / 60
        return render_to_response('show_oracle_rate.html', {'oracle_rate_list': oracle_rate_list,  'messageinfo_list': messageinfo_list,
                                                   'msg_num': msg_num,
                                                   'msg_last_content': msg_last_content, 'tim_last': tim_last})
    else:
        return render_to_response('show_oracle_rate.html', {'oracle_rate_list': oracle_rate_list})