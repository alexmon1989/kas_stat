from django.db import models


class DimTime(models.Model):
    timekey = models.PositiveIntegerField(db_column='TimeKey', primary_key=True)
    fulldatealternatekey = models.DateTimeField(db_column='FullDateAlternateKey', blank=True, null=True)
    daynumberofweek = models.IntegerField(db_column='DayNumberOfWeek', blank=True, null=True)
    ukrainiandaynameofweek = models.CharField(db_column='UkrainianDayNameOfWeek', max_length=10, blank=True, null=True)
    daynumberofmonth = models.IntegerField(db_column='DayNumberOfMonth', blank=True, null=True)
    daynumberofyear = models.SmallIntegerField(db_column='DayNumberOfYear', blank=True, null=True)
    weeknumberofyear = models.IntegerField(db_column='WeekNumberOfYear', blank=True, null=True)
    ukrainianmonthname = models.CharField(db_column='UkrainianMonthName', max_length=10, blank=True, null=True)
    monthnumberofyear = models.IntegerField(db_column='MonthNumberOfYear', blank=True, null=True)
    calendarquarter = models.IntegerField(db_column='CalendarQuarter', blank=True, null=True)
    calendaryear = models.IntegerField(db_column='CalendarYear', blank=True, null=True)
    calendarsemester = models.IntegerField(db_column='CalendarSemester', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_time'


class StatisticsValues(models.Model):
    cert = models.ForeignKey('StatisticsCertificates', on_delete=models.DO_NOTHING, db_column='idSertStat')
    timekey = models.ForeignKey('DimTime', db_column='TimeKey', on_delete=models.DO_NOTHING)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    value = models.IntegerField()
    iduser = models.PositiveIntegerField(db_column='idUser')
    claim = models.ForeignKey('LsClaimList', models.DO_NOTHING, db_column='claim_id', blank=True, null=True)
    objtype = models.ForeignKey('ClObjtypes', models.DO_NOTHING, db_column='obj_type_id')
    legalkind_id = models.IntegerField(db_column='legalKind_id', blank=True, null=True)  # Field name made lowercase.
    region = models.ForeignKey('ClRegion', on_delete=models.DO_NOTHING, blank=True, null=True, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'statistics_values'


class StatisticsCertificates(models.Model):
    certificate_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statistics_certificates'


class ClObjtypes(models.Model):
    idobjtype = models.AutoField(db_column='idObjType', primary_key=True)  # Field name made lowercase.
    objtype = models.CharField(db_column='ObjType', max_length=50)  # Field name made lowercase.
    glok_id = models.IntegerField(db_column='GLOK_ID', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cl_ObjTypes'


class LsClaimList(models.Model):
    idclaim = models.AutoField(db_column='idClaim', primary_key=True)  # Field name made lowercase.
    is_archived = models.PositiveIntegerField()
    claim_number = models.CharField(db_column='Claim_Number', max_length=50, blank=True, null=True)  # Field name made lowercase.
    objtype = models.ForeignKey('ClObjtypes', models.DO_NOTHING, db_column='idObjType')  # Field name made lowercase.
    certificate_number = models.CharField(max_length=50, blank=True, null=True)
    claim_date = models.DateTimeField(blank=True, null=True)
    certificate_date = models.DateTimeField(blank=True, null=True)
    num_decision = models.IntegerField(blank=True, null=True)
    date_decision = models.DateTimeField(blank=True, null=True)
    num_catalogue = models.IntegerField(blank=True, null=True)
    date_catalogue = models.DateTimeField(blank=True, null=True)
    num_bulletin = models.IntegerField(blank=True, null=True)
    date_bulletin = models.DateTimeField(blank=True, null=True)
    idstatus = models.IntegerField(db_column='idStatus', blank=True, null=True)  # Field name made lowercase.
    sub_status_id = models.PositiveIntegerField(blank=True, null=True)
    line = models.IntegerField(blank=True, null=True)
    personlinked = models.IntegerField(blank=True, null=True)
    line_dog = models.IntegerField(blank=True, null=True)
    personlinked_dog = models.IntegerField(blank=True, null=True)
    ap_names_aded = models.IntegerField(db_column='AP_names_aded', blank=True, null=True)  # Field name made lowercase.
    iduser = models.IntegerField(db_column='idUser', blank=True, null=True)  # Field name made lowercase.
    completion_date = models.DateField(blank=True, null=True)
    publishing_info = models.CharField(max_length=300, blank=True, null=True)
    derivative_work_info = models.CharField(max_length=300, blank=True, null=True)
    included_work_info = models.CharField(max_length=300, blank=True, null=True)
    iseapp = models.IntegerField(db_column='isEApp')  # Field name made lowercase.
    id_declarer = models.PositiveIntegerField(blank=True, null=True)
    bulletin_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    routeid = models.IntegerField()
    pathid = models.IntegerField()
    appnumber = models.CharField(db_column='appNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    persons = models.ManyToManyField('ClPersonList', through='LinkClaimPersons')
    oap = models.ManyToManyField('ClOap', through='LinkClaimOap')

    class Meta:
        managed = False
        db_table = 'ls_claim_list'


class ClPersonList(models.Model):
    idperson = models.AutoField(db_column='idPerson', primary_key=True)  # Field name made lowercase.
    person_legalform = models.IntegerField(blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    midle_name = models.CharField(max_length=50, blank=True, null=True)
    full_name = models.CharField(max_length=500, blank=True, null=True)
    short_name = models.CharField(max_length=200, blank=True, null=True)
    edrpou = models.CharField(db_column='EDRPOU', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ipn = models.CharField(db_column='IPN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    juridical_address = models.CharField(max_length=500, blank=True, null=True)
    post_address = models.CharField(max_length=500, blank=True, null=True)
    phones = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    www_site = models.CharField(max_length=100, blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    address_codes = models.CharField(max_length=255, blank=True, null=True)
    address_type = models.CharField(max_length=255, blank=True, null=True)
    claims = models.ManyToManyField('LsClaimList', through='LinkClaimPersons')

    class Meta:
        managed = False
        db_table = 'cl_person_list'


class LinkClaimPersons(models.Model):
    idlink = models.AutoField(primary_key=True)
    idclaim = models.ForeignKey('LsClaimList', models.DO_NOTHING, db_column='idClaim', blank=True, null=True)
    id_type_person = models.IntegerField(db_column='id_type_person', blank=True, null=True)
    idperson = models.ForeignKey('ClPersonList', models.DO_NOTHING, db_column='idPerson', blank=True, null=True)
    id_represent_form = models.IntegerField(db_column='id_represent_form', blank=True, null=True)
    alias_person = models.CharField(max_length=255, blank=True, null=True)
    contribution = models.CharField(max_length=300, blank=True, null=True)
    person_role = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link_claim_persons'


class LsEventList(models.Model):
    idevent = models.AutoField(primary_key=True)
    event_type = models.ForeignKey('ClEventClassif', models.DO_NOTHING, db_column='idevent_type', blank=True, null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    event_host = models.CharField(max_length=200, blank=True, null=True)
    idclaim = models.ForeignKey('LsClaimList', models.DO_NOTHING, db_column='idClaim', blank=True, null=True, related_name='events')
    iddoc = models.IntegerField(db_column='idDoc', blank=True, null=True)
    event_comment = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='idUser', blank=True, null=True)
    resolution = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ls_event_list'


class ClEventClassif(models.Model):
    idevent_type = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    bot_message = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cl_event_classif'


class Users(models.Model):
    role_id = models.PositiveIntegerField()
    active = models.PositiveIntegerField()
    banned = models.PositiveIntegerField()
    hash = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    personal_number = models.CharField(max_length=16, blank=True, null=True)
    subdivision = models.CharField(max_length=256, blank=True, null=True)
    position = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
        unique_together = (('last_name', 'first_name', 'middle_name'),)


class ClOapTypes(models.Model):
    id_oap_type = models.AutoField(db_column='id_OAP_type', primary_key=True)  # Field name made lowercase.
    oap_type_name = models.CharField(db_column='OAP_type_name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cl_OAP_types'


class ClOap(models.Model):
    idoap = models.AutoField(db_column='idOAP', primary_key=True)  # Field name made lowercase.
    oap_name = models.CharField(db_column='OAP_name', max_length=200, blank=True, null=True)  # Field name made lowercase.
    id_oap_type = models.ForeignKey('ClOapTypes', models.DO_NOTHING, db_column='id_OAP_type', blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(blank=True, null=True)
    claims = models.ManyToManyField('LsClaimList', through='LinkClaimOap')

    class Meta:
        managed = False
        db_table = 'cl_OAP'


class LinkClaimOap(models.Model):
    idlinkoap = models.AutoField(db_column='idLinkOAP', primary_key=True)  # Field name made lowercase.
    idoap = models.ForeignKey('ClOap', models.DO_NOTHING, db_column='idOAP', blank=True, null=True)  # Field name made lowercase.
    idclaim = models.ForeignKey('LsClaimList', models.DO_NOTHING, db_column='idClaim', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'link_claim_OAP'


class ClRegion(models.Model):
    id_region = models.AutoField(primary_key=True)
    region = models.CharField(unique=True, max_length=255, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cl_regions'
