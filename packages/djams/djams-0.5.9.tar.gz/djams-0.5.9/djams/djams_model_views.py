class View_User_Authorized_Apps(models.Model):
    user_id = models.BigIntegerField()
    app_id = models.BigIntegerField()
    app_name = models.CharField(max_length=200, null=True, blank=False)
    username = models.CharField(max_length=200, null=True, blank=True)
    user_first_name = models.CharField(max_length=100, null=True, blank=True)
    user_last_name = models.CharField(max_length=100, null=True, blank=True)
    user_email = models.CharField(max_length=200, null=True, blank=True)
    app_version = models.CharField(max_length=30, null=True, blank=True)
    django_app_name = models.CharField(max_length=100, null=True, blank=True)
    launch_view = models.CharField(max_length=200, null=True, blank=True)
    launch_url = models.CharField(max_length=200, null=True, blank=True)
    launch_local_url = models.CharField(max_length=200, null=True, blank=True)
    launch_dev_url = models.CharField(max_length=200, null=True, blank=True)
    launch_qa_url = models.CharField(max_length=200, null=True, blank=True)
    launch_uat_url = models.CharField(max_length=200, null=True, blank=True)
    launch_prod_url = models.CharField(max_length=200, null=True, blank=True)
    app_thumbnail = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'View_User_Authorized_Apps'
        app_label = 'view_authorities'

class View_UserClients(models.Model):
    user_id = models.BigIntergerField():
    registered_name = models.CharField(max_length=100, null=True, blank=False)
    short_name = models.CharField(max_length=100, null=True, blank=False)
    client_database = models.CharField(max_length=100, null=True, blank=False)
    logo = models.CharField(max_length=100, null=True, blank=False)
    client_id = models.BigIntegerField()
    app_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'UserClients'
        app_label = 'view_user_clients' 

