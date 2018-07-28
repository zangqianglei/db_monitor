from django.db import models

# Create your models here.

class OracleDb(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    dbname = models.CharField(max_length=255, blank=True, null=True)
    db_unique_name = models.CharField(max_length=255, blank=True, null=True)
    database_role = models.CharField(max_length=255, blank=True, null=True)
    open_mode = models.CharField(max_length=255, blank=True, null=True)
    log_mode = models.CharField(max_length=255, blank=True, null=True)
    archive_used = models.CharField(max_length=255, blank=True, null=True)
    archive_rate_level = models.CharField(max_length=255, blank=True, null=True)
    inst_id = models.IntegerField(blank=True, null=True)
    instance_name = models.CharField(max_length=255, blank=True, null=True)
    host_name = models.CharField(max_length=255, blank=True, null=True)
    max_process = models.IntegerField(blank=True, null=True)
    current_process = models.IntegerField(blank=True, null=True)
    percent_process = models.CharField(max_length=255, blank=True, null=True)
    conn_rate_level = models.CharField(max_length=255, blank=True, null=True)
    adg_transport_lag = models.CharField(max_length=255, blank=True, null=True)
    adg_apply_lag = models.CharField(max_length=255, blank=True, null=True)
    adg_transport_value = models.IntegerField(blank=True, null=True)
    adg_transport_rate_level = models.CharField(max_length=255, blank=True, null=True)
    adg_apply_value = models.IntegerField(blank=True, null=True)
    adg_apply_rate_level = models.CharField(max_length=255, blank=True, null=True)
    mon_status = models.CharField(max_length=255)
    err_info = models.TextField(blank=True, null=True)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_db'


class OracleDbEvent(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    event_no = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255)
    event_cnt = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_db_event'


class OracleDbHis(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    dbname = models.CharField(max_length=255, blank=True, null=True)
    db_unique_name = models.CharField(max_length=255, blank=True, null=True)
    database_role = models.CharField(max_length=255, blank=True, null=True)
    open_mode = models.CharField(max_length=255, blank=True, null=True)
    inst_id = models.IntegerField(blank=True, null=True)
    instance_name = models.CharField(max_length=255, blank=True, null=True)
    host_name = models.CharField(max_length=255, blank=True, null=True)
    max_process = models.IntegerField(blank=True, null=True)
    current_process = models.IntegerField(blank=True, null=True)
    percent_process = models.CharField(max_length=255, blank=True, null=True)
    conn_rate_level = models.CharField(max_length=255, blank=True, null=True)
    adg_transport_lag = models.CharField(max_length=255, blank=True, null=True)
    adg_apply_lag = models.CharField(max_length=255, blank=True, null=True)
    adg_transport_value = models.IntegerField(blank=True, null=True)
    adg_transport_rate_level = models.CharField(max_length=255, blank=True, null=True)
    adg_apply_value = models.IntegerField(blank=True, null=True)
    adg_apply_rate_level = models.CharField(max_length=255, blank=True, null=True)
    mon_status = models.CharField(max_length=255)
    err_info = models.TextField(blank=True, null=True)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_db_his'


class OracleDbRate(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    conn_decute = models.IntegerField()
    tbs_decute = models.IntegerField()
    undo_decute = models.IntegerField()
    tmp_decute = models.IntegerField()
    cpu_decute = models.IntegerField()
    mem_decute = models.IntegerField()
    disk_decute = models.IntegerField()
    adg_decute = models.IntegerField()
    db_rate = models.IntegerField()
    db_rate_level = models.CharField(max_length=255, blank=True, null=True)
    db_rate_color = models.CharField(max_length=255, blank=True, null=True)
    db_rate_reason = models.CharField(max_length=255, blank=True, null=True)
    rate_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_db_rate'


class OracleDbRateHis(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    dbname_cn = models.CharField(max_length=255)
    conn_decute = models.IntegerField()
    tbs_decute = models.IntegerField()
    undo_decute = models.IntegerField()
    tmp_decute = models.IntegerField()
    cpu_decute = models.IntegerField()
    mem_decute = models.IntegerField()
    disk_decute = models.IntegerField()
    adg_decute = models.IntegerField()
    db_rate = models.IntegerField()
    db_rate_level = models.CharField(max_length=255, blank=True, null=True)
    db_rate_color = models.CharField(max_length=255, blank=True, null=True)
    db_rate_reason = models.CharField(max_length=255, blank=True, null=True)
    rate_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_db_rate_his'


class OracleLock(models.Model):
    tags = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    session = models.CharField(max_length=255)
    lmode = models.CharField(max_length=255)
    ctime = models.CharField(max_length=255)
    inst_id = models.CharField(max_length=255)
    lmode1 = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    chk_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oracle_lock'


class OracleInvalidIndex(models.Model):
    tags = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    index_name = models.CharField(max_length=255)
    partition_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    chk_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oracle_invalid_index'


class OracleTbs(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    service_name = models.CharField(max_length=255)
    tbs_name = models.CharField(max_length=255)
    datafile_count = models.IntegerField()
    size_gb = models.CharField(max_length=32)
    free_gb = models.CharField(max_length=32)
    used_gb = models.CharField(max_length=32)
    max_free = models.CharField(max_length=32)
    pct_used = models.CharField(max_length=32)
    pct_free = models.CharField(max_length=32)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_tbs'


class OracleTbsHis(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    service_name = models.CharField(max_length=255)
    tbs_name = models.CharField(max_length=255)
    datafile_count = models.IntegerField()
    size_gb = models.CharField(max_length=32)
    free_gb = models.CharField(max_length=32)
    used_gb = models.CharField(max_length=32)
    max_free = models.CharField(max_length=32)
    pct_used = models.CharField(max_length=32)
    pct_free = models.CharField(max_length=32)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_tbs_his'


class OracleTmpTbs(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    tmp_tbs_name = models.CharField(max_length=255)
    total_mb = models.CharField(max_length=255)
    used_mb = models.CharField(max_length=255)
    pct_used = models.CharField(max_length=255)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_tmp_tbs'


class OracleTmpTbsHis(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    tmp_tbs_name = models.CharField(max_length=255)
    total_mb = models.CharField(max_length=255)
    used_mb = models.CharField(max_length=255)
    pct_used = models.CharField(max_length=255)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_tmp_tbs_his'


class OracleUndoTbs(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    undo_tbs_name = models.CharField(max_length=255)
    total_mb = models.CharField(max_length=255)
    used_mb = models.CharField(max_length=255)
    pct_used = models.CharField(max_length=255)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_undo_tbs'


class OracleUndoTbsHis(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    undo_tbs_name = models.CharField(max_length=255)
    total_mb = models.CharField(max_length=255)
    used_mb = models.CharField(max_length=255)
    pct_used = models.CharField(max_length=255)
    rate_level = models.CharField(max_length=255)
    chk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oracle_undo_tbs_his'


class TabOracleServers(models.Model):
    tags = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    service_name = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_os = models.CharField(max_length=255)
    password_os = models.CharField(max_length=255)
    connect = models.CharField(max_length=255)
    connect_cn = models.CharField(max_length=255)
    tbs = models.CharField(max_length=255)
    tbs_cn = models.CharField(max_length=255)
    adg = models.CharField(max_length=255)
    adg_cn = models.CharField(max_length=255)
    temp_tbs = models.CharField(max_length=255)
    temp_tbs_cn = models.CharField(max_length=255)
    undo_tbs = models.CharField(max_length=255)
    undo_tbs_cn = models.CharField(max_length=255)
    conn = models.CharField(max_length=255)
    conn_cn = models.CharField(max_length=255)
    err_info = models.CharField(max_length=255)
    err_info_cn = models.CharField(max_length=255)
    invalid_index = models.CharField(max_length=255)
    invalid_index_cn = models.CharField(max_length=255)
    oracle_lock = models.CharField(max_length=255)
    oracle_lock_cn = models.CharField(max_length=255)
    oracle_pwd = models.CharField(max_length=255)
    oracle_pwd_cn = models.CharField(max_length=255)
    pga = models.CharField(max_length=255)
    pga_cn = models.CharField(max_length=255)
    archive = models.CharField(max_length=255)
    archive_cn = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tab_oracle_servers'