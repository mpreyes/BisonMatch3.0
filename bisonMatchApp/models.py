# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Lustudent(models.Model):
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    lnumber = models.CharField(db_column='LNumber', max_length=255,primary_key = True)  # Field name made lowercase.
    emailaddress = models.CharField(db_column='EmailAddress', max_length=256)  # Field name made lowercase.
    major = models.CharField(db_column='Major', max_length=50)
    bio = models.CharField(db_column='Bio', max_length=256)  # Field name made lowercase.
    idealdate = models.CharField(db_column='IdealDate', max_length=256)
    gender = models.IntegerField(db_column='Gender')  # Field name made lowercase.
    ans1 = models.IntegerField(db_column='Ans1')  # Field name made lowercase.
    ans2 = models.IntegerField(db_column='Ans2')  # Field name made lowercase.
    ans3 = models.IntegerField(db_column='Ans3')  # Field name made lowercase.
    ans4 = models.IntegerField(db_column='Ans4')  # Field name made lowercase.
    ans5 = models.IntegerField(db_column='Ans5')  # Field name made lowercase.
    ans6 = models.IntegerField(db_column='Ans6')  # Field name made lowercase.
    ans7 = models.IntegerField(db_column='Ans7')  # Field name made lowercase.
    ans8 = models.IntegerField(db_column='Ans8')  # Field name made lowercase.
    ans9 = models.IntegerField(db_column='Ans9')  # Field name made lowercase.
    ans10 = models.IntegerField(db_column='Ans10')  # Field name made lowercase.
    profilepicurl = models.CharField(db_column='ProfilePicUrl', max_length=2083)  # Field name made lowercase.
    paid = models.IntegerField(db_column="Paid")

    class Meta:
        managed = True
        db_table = 'LUStudent'

class StudentMatches(models.Model):
    id = models.AutoField(db_column='ID', primary_key = True)
    studentlnumber = models.CharField(db_column='StudentLNumber', max_length=255)
    matchlnumber = models.CharField(db_column='MatchLNumber', max_length=255)

    class Meta:
        managed = True
        db_table = 'StudentMatches'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class ImageUpload(models.Model):
    media = models.FileField(upload_to="user_profiles")
