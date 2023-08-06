'''
Base master models for analytical microsite apps as well as bindings to create an application portal with models such as the App model and the Authority model, which controls user 
specific access to apps on a per client basis.  
'''

import json
import os
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
import uuid
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class ADM_CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'djams'

class MDS_CountryGroup(models.Model):
    '''
    Description: Examples include countries that are members of the OECD, NAFTA, EU, EFTA, Eurozone and Schengen
    '''

    name = models.CharField(max_length=200, null=False, blank=False)
    abbreviation = models.CharField(max_length=20, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="countrygroup_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='countrygroup_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:countrygroup-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:countrygroup-del', arg[str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'


class MDS_Country(models.Model):
    '''
    Description: Master country data
    '''

    name = models.CharField(max_length=200, null=False, blank=False)
    capital_city = models.CharField(max_length=200, null=True, blank=True)
    iso_numeric = models.IntegerField(null=True, blank=True)
    iso_alpha2 = models.CharField(max_length=2, null=False, blank=False)
    iso_alpha3 = models.CharField(max_length=3, null=False, blank=False)
    iso_version = models.CharField(max_length=30, null=True, blank=False)

    valid_from_date = models.DateField(blank=True, null=False)
    valid_to_date = models.DateField(blank=True, null=True)
    latest_version = models.BooleanField(default=False)
    group_membership = models.ManyToManyField(MDS_CountryGroup)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="country_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='country_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:country-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:country-del', arg[str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'
        ordering = (['id'])




class MDS_PartyClass(models.Model):
    description = models.CharField(max_length=50, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="partyclass_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='partyclass_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:partyclass-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:partyclass-del', arg[str(self.id)])

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'djams'


class MDS_PartyType(models.Model):
    description = models.CharField(max_length=100, null=False, blank=False)
    abbreviation = models.CharField(max_length=20, null=False, blank=False)
    country = models.ForeignKey(MDS_Country, related_name='partytype_country', on_delete=models.SET_NULL, null=True, blank=True)
    partyclass = models.ForeignKey(MDS_PartyClass, related_name='partytype_partyclass', on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="partytype_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='partytype_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:partyclass-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:partyclass-del', arg[str(self.id)])

    def __str__(self):
        return self.description

    class Meta:
        app_label = 'djams'

# class MDS_Party(models.Model):

#     '''
#     Description: Includes the types of party to a transaction (e.g. an indiviual, partnership, trust, company etc.). 
#     '''

#     gfis_id = models.CharField(max_length=50, null=False, blank=False)
#     registered_country = models.ForeignKey(MDS_Country, related_name='party_country', on_delete=models.CASCADE)
#     party_type = models.ForeignKey(MDS_PartyType, related_name='party_party_type', on_delete=models.SET_NULL, null=True, blank=False)
#     creation_date = models.DateField(auto_now_add=True, blank=True)
#     creation_user = models.ForeignKey(ADM_CustomUser, related_name="party_creator", on_delete=models.SET_NULL, null=True, blank=True)
#     last_update_date = models.DateField(auto_now=True, blank=True)
#     last_update_user = models.ForeignKey(ADM_CustomUser, related_name='party_updater', on_delete=models.SET_NULL, null=True, blank=True)

#     def get_absolute_url_groupadd(self):
#         return reverse('admin_portal:party-add', arg[str(self.id)])

#     def get_absolute_url_regionadd(self):
#         return reverse('admin_portal:party-add', arg[str(self.id)])

#     def __str__(self):
#         return str(self.id)

#     class Meta:
#         app_label = 'djams'

class MDS_Company_Manager(models.Manager):
    def get_by_natural_key(self, registered_name):
        return self.get(registered_name=registered_name)

class MDS_Company(models.Model):
    '''
    Description: Company information. This could be client info or info about the organisation. This is used for purposes such as company info but critically database routing, which is typically required for apps that are utilised for multiple clients. 
    '''
    objects = MDS_Company_Manager()

    #party = models.OneToOneField(MDS_Party, on_delete=models.CASCADE)
    registered_name = models.CharField(max_length=200, null=False, blank=False)
    gfis_id = models.CharField(max_length=50, null=True, blank=True)
    registered_country = models.ForeignKey(MDS_Country, related_name='party_country', on_delete=models.CASCADE)
    party_type = models.ForeignKey(MDS_PartyType, related_name='party_party_type', on_delete=models.SET_NULL, null=True, blank=False)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    database_name = models.CharField(unique=True, max_length=200, help_text='Enter the name of the client specific SQL database')
    logo = models.ImageField(upload_to='company_thumbnails', null=True, blank=True, verbose_name="Company Logo Thumbnail", default="company_thumbnails/media.jpg")

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="company_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='company_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:company-edit', arg[str(self.party_id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:company-del', arg[str(self.party_id)])

    def __str__(self):
        return str(self.registered_name)

    def natural_key(self):
        return (self.registered_name)

    class Meta:
        app_label = 'djams'
        ordering = (['registered_name'])

class MDS_Currency(models.Model):
    name = models.CharField(max_length=75)
    iso_alpha3 = models.CharField(max_length=3, null=True, blank=True)
    iso_numeric = models.IntegerField(null=True, blank=True)
    symbol = models.CharField(max_length=20, null=True, blank=True)
    minor_unit = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey(MDS_Country, related_name="currency_country", on_delete=models.SET_NULL, null=True, blank=True)
    valid_from_date = models.DateField(blank=True, null=True)
    valid_to_date = models.DateField(blank=True, null=True)
    latest_version = models.BooleanField(default='True')

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="currency_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='currency_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:currency-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:currency-del', arg[str(self.id)])

    def __str__(self):
        return "%s (%s)" %(str(self.name), str(self.symbol))

    class Meta:
        app_label = 'djams'
        ordering = (['name'])

class MDS_TaxType(models.Model):
    '''
    Description: Standardized defitions of tax types used in apps for tax calculation purposes
    '''
   
    REGION_TYPES = (
                    ('l', 'Local Government Tax'),
                    ('s', 'State Tax'), 
                    ('n', 'National/Federal Tax'),
                   )
    generic_tax_type_name = models.CharField(max_length=200, null=False, blank=False)
    generic_tax_type_abbr = models.CharField(max_length=10, null=True, blank=True)
    tax_region = models.CharField(max_length=200, null=False, blank=False, choices=REGION_TYPES)
    tax_category = models.CharField(max_length=200, null=True, blank=False)
    region_specific_tax_type_name = models.CharField(max_length=200, null=True, blank=False)
    specific_tax_type_abbr = models.CharField(max_length=10, null=True, blank=True)
    jurisdiction = models.ForeignKey(MDS_Country, null=True, blank=True, on_delete=models.SET_NULL)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="taxtype_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='taxtype_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:taxtype-edit', arg[str(self.party_id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:taxtype-del', arg [str(self.party_id)])

    def __str__(self):
        return str(self.generic_tax_type_name)

    class Meta:
        app_label = 'djams'

class MDS_FinancialInstrumentType(models.Model):
    '''
    Description: Standardized definitions of financial instrument types used in apps.
    '''

    REGION_TYPES = (
                    ('n', 'National'),
                    ('c', 'Continental'),
                    ('i', 'International'),
                    )

    generic_instrument_type_name = models.CharField(max_length=200, null=False, blank=False)
    generic_instrument_type_abbreviation = models.CharField(max_length=20, null=True, blank=True)
    instrument_region = models.CharField(max_length=200, null=False, blank=False, choices=REGION_TYPES)
    tax_category = models.CharField(max_length=200, null=True, blank=False)
    region_specific_instrument_type_name = models.CharField(max_length=200, null=True, blank=False)
    specific_instrument_type_abbr = models.CharField(max_length=20, null=True, blank=True)
    jurisdiction = models.ForeignKey(MDS_Country, null=True, blank=True, on_delete=models.SET_NULL)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="fininsttype_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='fininsttype_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:fininsttype-edit', arg[str(self.party_id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:fininsttype-del', arg [str(self.party_id)])

    def __str__(self):
        return str(self.generic_tax_type_name)

    class Meta:
        app_label = 'djams'

class ADM_AppCategoryType(models.Model):
    '''
    Description: The categorys of types of app
    '''
    description = models.CharField(max_length=200, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="appcategorytype_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='appcategorytype_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:appcategorytype-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:appcategorytype-del', arg [str(self.id)])

    def __str__(self):
        return str(self.description)

    class Meta:
        app_label = 'djams'

class ADM_AppCategory(models.Model):
    app_category_type = models.ForeignKey(ADM_AppCategoryType, related_name="appcategory_type", on_delete=models.SET_NULL, null=True, blank=True)
    keyword = models.CharField(max_length=150, null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="appcategory_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='appcategory_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:appcategory-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:appcategory-del', arg [str(self.id)])

    def __str__(self):
        return str(self.app_category_type)

    class Meta:
        app_label = 'djams'


loc = os.path.join(settings.BASE_DIR, settings.SERVER_SETTINGS_DICT[settings.SERVER_ENV]['SHARED_MEDIA_LOC'])
shared_image_fs = FileSystemStorage(location=loc)

class ADM_App(models.Model):
    '''
    Description: Captures information about the App available to a user.
    ''' 
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="App Name")
    description = models.CharField(max_length=350, null=True, blank=True, verbose_name="Description")
    django_app_name = models.CharField(unique=True, max_length=150, null=True, blank=False, verbose_name='Django App Name',
                                        error_messages={'unique':"This django_app_name has already been taken."})
    version = models.DecimalField(null=True, blank=True, verbose_name="App Version", decimal_places=2, max_digits=5)
    user_launch_view = models.CharField(max_length=200, null=True, blank=True, verbose_name="Launch View")
    launch_url = models.URLField(null=True, blank=True)
    launch_local_url = models.URLField(null=True, blank=True)
    launch_integrated_apps_url = models.CharField(max_length=150, null=True, blank=False)
    launch_dev_url = models.URLField(null=True, blank=True)
    launch_qa_url = models.URLField(null=True, blank=True)
    launch_uat_url = models.URLField(null=True, blank=True)
    launch_prod_url = models.URLField(null=True, blank=True)
    tax_type = models.ManyToManyField(MDS_TaxType, verbose_name="Tax Type", blank=True)
    instrument_category = models.ManyToManyField(MDS_FinancialInstrumentType, verbose_name="Financial Instrument Category", blank=True)
    app_category = models.ManyToManyField(ADM_AppCategory, verbose_name="App Categories", blank=True)

    support_start_date = models.DateField(null=True, blank=True, verbose_name="Support Start Date")
    support_end_date = models.DateField(null=True, blank=True, verbose_name="Support End Date")
    billing_recipient = models.ForeignKey(ADM_CustomUser, related_name="billing_recipient", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Billing Recipient")
    sales_contact = models.ForeignKey(ADM_CustomUser, related_name="sales_contact", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sales Contact")
    tech_expert = models.ForeignKey(ADM_CustomUser, related_name="tech_solution_expert", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Technology Solution Expert")
    tax_sme = models.ForeignKey(ADM_CustomUser, related_name="tax_sme", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tax SME")
    finance_sme = models.ForeignKey(ADM_CustomUser, related_name="finance_sme", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Finance SME")
    
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="app_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='app_updater', on_delete=models.SET_NULL, null=True, blank=True)

    app_thumbnail = models.ImageField(upload_to='app_thumbnails', storage=shared_image_fs)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:app-edit', arg[str(self.id)])

    def get_absolute_url_delete(self):
        return reverse('admin_portal:app-del', arg [str(self.id)])

    def get_absolute_url_new(self):
        return reverse('admin_portal:app-new')

    def get_absolute_microsite_url_redirect(self):
        '''
        Description: This is for microsite redirects using an app portal. This ensures each app is in its own container and doesn't interfere with other apps.
        '''
        return str(self.launch_url)

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'

class ADM_AppRole(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="approle_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='approle_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:approle-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:approle-del', arg [str(self.id)])

    def __str__(self):
        return str(self.app_category_type)

    class Meta:
        app_label = 'djams'
        ordering=(['name'])

class ADM_UserAppRole(models.Model):
    user = models.ForeignKey(ADM_CustomUser, related_name="userapprole_user", on_delete=models.SET_NULL, null=True, blank=True)
    app = models.ForeignKey(ADM_App, related_name="userapprole_app", on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(ADM_AppRole, related_name="userapprole_role", on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="userapprole_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='userapprole_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:userapprole-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:userapprole-del', arg [str(self.id)])

    def __str__(self):
        return "%s:%s:%s" %(str(self.user.username), str(self.app.name), str(self.role.name))

    class Meta:
        app_label = 'djams'
        ordering=(['user', 'app', 'role'])

class ADM_Team(models.Model):
    '''
    Description: App User Team
    '''

    name = models.CharField(max_length=200, null=False, blank=False)
    team_members = models.ManyToManyField(ADM_CustomUser, related_name='team_members_users')
    team_lead = models.ForeignKey(ADM_CustomUser, related_name="team_lead_user", on_delete=models.SET_NULL, null=True, blank=True)
    deputy_team_lead = models.ForeignKey(ADM_CustomUser, related_name="dep_team_lead_user", on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="team_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='team_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:team-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:team-del', arg [str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'


class ADM_DevTeam(models.Model):
    '''
    Description: App Development Teams
    '''

    name = models.CharField(max_length=200, null=False, blank=False)
    team_lead = models.ForeignKey(ADM_CustomUser, related_name="devteam_lead_user", on_delete=models.SET_NULL, null=True, blank=True)
    team_members = models.ManyToManyField(ADM_CustomUser, related_name='devteam_members_users')
    deputy_team_lead = models.ForeignKey(ADM_CustomUser, related_name="devteam_dep_lead_user", on_delete=models.SET_NULL, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="devteam_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='devteam_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:devteam-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:devteam-del', arg [str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'

class ADM_SelfServiceUser(models.Model):
    '''
    Description: App Development Teams
    '''

    email = models.CharField(max_length=200, null=False, blank=False)
    user = models.ForeignKey(ADM_CustomUser, related_name="selfserviceuser_user", on_delete=models.CASCADE, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    dev_account = models.CharField(max_length=100, null=False, blank=False)
    team = models.ForeignKey(ADM_Team, related_name="selfserviceuser_team", on_delete=models.SET_NULL, null=True, blank=True)
    dev_team = models.ForeignKey(ADM_DevTeam, related_name="selfserviceuser_devteam", on_delete=models.SET_NULL, null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="selfserviceuser_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='selfserviceuser_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:selfserviceuser-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:selfserviceuser-del', arg [str(self.id)])

    def __str__(self):
        return str(self.email)

    class Meta:
        app_label = 'djams'




class ADM_SubscriptionType(models.Model):
    '''
    Description: App subscription types
    '''

    SUBSCRIPTION_DURATIONS = (('m', 'Monthly'), ('a', 'Annual'), ('c', 'Custom Fee'))

    name = models.CharField(max_length=200, null=False, blank=False)
    length = models.CharField(max_length=2, null=True, blank=True, choices=SUBSCRIPTION_DURATIONS)
    days_subscribed = models.IntegerField(null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="subscriptiontype_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='subscriptiontype_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:subscriptiontype-edit', arg[str(self.id)])

    def get_absolute_url_detail(self):
        return reverse('admin_portal:subscriptiontype-detail', arg [str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:subscriptiontype-del', arg [str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'
        ordering = (['name'])

class ADM_Subscription(models.Model):
    '''
    Description: Sets a subscription of a company / client to an app. No automated payment is implemented in the app yet.
    '''

    client = models.ForeignKey(MDS_Company, related_name="subscription_party", on_delete=models.SET_NULL, null=True, blank=True)
    app = models.ForeignKey(ADM_App, related_name='subscription_solution', on_delete=models.SET_NULL, null=True, blank=True)
    subscription_type = models.ForeignKey(ADM_SubscriptionType, related_name="substype_subs", on_delete=models.SET_NULL, null=True, blank=True)
    subscription_paid = models.BooleanField(default=False)
    subscription_paid_currency = models.ForeignKey(MDS_Currency, related_name="subscription_currency", on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=38, decimal_places=2)
    uses_regions = models.BooleanField(default=True)
    uses_groups = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    currently_subscribed = models.BooleanField(default=False)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="subscription_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='subscription_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:subscription-edit', arg[str(self.id)])

    def get_absolute_url_detail(self):
        return reverse('admin_portal:subscription-detail', arg [str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:subscription-del', arg [str(self.id)])

    def __str__(self):
        return "%s:%s" %(str(self.client), str(self.app))

    class Meta:
        app_label = 'djams'
        ordering = (['app'])

class ADM_EnquiryStatus(models.Model):
    '''
    Description: Definitions of the various status types of a user enquiry in relation to an app or apps
    '''
    name = models.CharField(max_length=200, null=False, blank=False)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="enquiry_status_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='enquiry_status_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:enquirystatus-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:enquirystatus-del', arg [str(self.id)])

    def __str__(self):
        return "%s" %(str(self.name))

    class Meta:
        app_label = 'djams'

class ADM_UserEnquiry(models.Model):
    '''
    Description: Allows authenticated or anonymous users to post an enquiry 
    '''
    reference = models.TextField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(ADM_CustomUser, related_name="userenquiry_user", on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(ADM_Team, related_name="userenquiry_team", on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(MDS_Company, related_name="userenquiry_company", on_delete=models.SET_NULL, null=True, blank=True)
    app = models.ForeignKey(ADM_App, related_name="userenquiry_app", on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(max_length=2000, help_text="Enter your enquiry here", null=True)
    status = models.ForeignKey(ADM_EnquiryStatus, related_name="userenquiry_enquirystatus", on_delete=models.SET_NULL, null=True, blank=True)
    status_datetime_changed = models.DateTimeField(null=True, blank=True)
    opened_date = models.DateField(auto_now=True)
    closed_date = models.DateField(null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="userenquiry_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='userenquiry_status_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:userenquiry-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:userenquiry-del', arg [str(self.id)])

    def __str__(self):
        return "%s, (%s)" %(str(self.user), str(self.opened_date))

    class Meta:
        app_label = 'djams'

class ADM_EnquiryMessage(models.Model):
    '''
    Description: Records the messages exchanged over an individual message thread 
    '''
    enquiry_thread = models.ForeignKey(ADM_UserEnquiry, related_name="enquirymessage_userenquiry", on_delete=models.SET_NULL, null=True, blank=True)
    message_author = models.ForeignKey(ADM_CustomUser, related_name="enquirymessage_user", on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(ADM_Team, related_name="enquirymessage_team", on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(max_length=2000, null=True)
    message_read = models.BooleanField(default='False')
    team_responded = models.BooleanField(default=False)
    enquirer_responded = models.BooleanField(default=False)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="enquirymessage_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='enquirymessage_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('admin_portal:usrenq-dialogue', arg[str(self.enquiry)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:enquiry-del', arg [str(self.enquiry)])

    def __str__(self):
        return "%s, (%s)" %(str(self.message))

    class Meta:
        app_label = 'djams'
        ordering = ['creation_date']

class MDS_ClientRegion(models.Model):

    '''
    Description: Describes the combination of countries that a client specifies as a region. For example, EMEIA is a specified group of countries but is not used by all companies
    '''
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    client = models.ForeignKey(MDS_Company, related_name="clientregion_company", on_delete=models.SET_NULL, null=True, blank=True)
    countries = models.ManyToManyField(MDS_Country)
    valid_from_date = models.DateField(blank=True, null=True)
    valid_to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="clientregion_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='clientregion_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:clientregion-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:clientregion-del', arg [str(self.id)])

    def __str__(self):
        return "%s, (%s)" %(str(self.name))

    class Meta:
        app_label = 'djams'
        ordering = ['name']

class MDS_ClientGroup(models.Model):

    '''
    Description: Arbitrary client specified groups for controlling access to data. A group could be HQ, derivatives trading department, tax department etc.
    '''
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    client = models.ForeignKey(MDS_Company, related_name="clientgroup_company", on_delete=models.SET_NULL, null=True, blank=True)
    countries = models.ManyToManyField(MDS_Country)
    valid_from_date = models.DateField(blank=True, null=True)
    valid_to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="clientgroup_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='clientgroup_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:clientgroup-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:clientgroup-del', arg [str(self.id)])

    def __str__(self):
        return "%s" %(str(self.name))

    class Meta:
        app_label = 'djams'
        ordering = ['name']

class ADM_Authority(models.Model):
    '''
    Description: The Authority model drives the access definitions for user, client and app combinations. e.g. user X may access app Y for client Z. This maintains data security as well controls app permissions. 
    '''

    client = models.ForeignKey(MDS_Company, related_name="authority_company", on_delete=models.SET_NULL, null=True, blank=True)
    subscription = models.ForeignKey(ADM_Subscription, related_name="authority_subscription", on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(ADM_CustomUser, related_name="authority_user", on_delete=models.SET_NULL, null=True, blank=True)
    app = models.ForeignKey(ADM_App, related_name="authority_app", on_delete=models.SET_NULL, null=True, blank=True)
    regions_used = models.BooleanField(default=False)
    groups_used = models.BooleanField(default=False)
    client_group = models.ForeignKey(MDS_ClientGroup, related_name="authority_clientgroup", on_delete=models.SET_NULL, null=True, blank=True)
    client_region = models.ForeignKey(MDS_ClientRegion, related_name="authority_clientregion", on_delete=models.SET_NULL, null=True, blank=True)

    valid_from_date = models.DateField(blank=True, null=True)
    valid_to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="authority_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='authority_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:userauthorization-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:userauthorization-del', arg [str(self.id)])

    def get_absolute_launch_url(self):
        return reverse("%s:%s" %(str(self.app.name), self.app.user_launch_view), arg [str(self.client.id)])

    def __str__(self):
        return "%s - %s - %s" %(str(self.client.gfis_id), str(self.app.name), str(self.user.username))

    class Meta:
        app_label = 'djams'
        ordering = ['client', 'user', 'app']

class ADM_EventType(models.Model):
    '''
    Description: Types of audit events logged
    '''
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return "%s" %(str(self.name))

    class Meta:
        app_label = 'djams'

class MDS_PublicBodyType(models.Model):
    '''
    Description: Types of public bodies
    '''
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=300, null=False, blank=False)

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="publicbodytype_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='publicbodytype_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:publicbodytype-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:pbulicbodytype-del', arg [str(self.id)])

    def __str__(self):
        return "%s" %(str(self.name))

    class Meta:
        app_label = 'djams'


class MDS_PublicBody(models.Model):
    '''
    Description: Types of public bodies
    '''
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    body_type = models.ForeignKey(MDS_PublicBodyType, related_name="publicbody_publicbodytype", on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ManyToManyField(MDS_Country, related_name="publicbody_country")

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="publicbody_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='publicbody_updater', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:publicbody-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:publicbody-del', arg [str(self.id)])

    def __str__(self):
        return "%s" %(str(self.name))

    class Meta:
        app_label = 'djams'


class ADM_AppSession(models.Model):
    '''
    Description: Records of initial and end of app sessions
    '''
    token = models.CharField(max_length=150, null=True, blank=True)
    user = models.ForeignKey(ADM_CustomUser, related_name="appsession_user", on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    client = models.ForeignKey(MDS_Company, related_name="appsession_client", on_delete=models.SET_NULL, null=True)
    app_name = models.CharField(max_length=150, null=True, blank=True)
    app = models.ForeignKey(ADM_App, related_name="appsession_app", on_delete=models.SET_NULL, null=True, blank=True)
    event_time = models.DateTimeField(null=True, blank=True)
    user_ip = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'djams'

class ADM_AppSessionAudit(models.Model):
    '''
    Description: Records of app actions for audit purposes
    '''
    token = models.CharField(max_length=150, null=True, blank=True)
    user = models.ForeignKey(ADM_CustomUser, related_name="appsession_user_audit", on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    client = models.ForeignKey(MDS_Company, related_name="appsessionaudit_client", on_delete=models.SET_NULL, null=True, blank=True)
    app_name = models.CharField(max_length=150, null=True, blank=True)
    app = models.ForeignKey(ADM_App, related_name="appsessionaudit_app", on_delete=models.SET_NULL, null=True, blank=True)
    event_time = models.DateTimeField(null=True, blank=True)
    event_result = models.CharField(max_length=100, null=True, blank=True)
    operating_user = models.ForeignKey(ADM_CustomUser, related_name="appsessionaudit_user", on_delete=models.SET_NULL, null=True, blank=True)
    operating_username = models.CharField(max_length=150, null=True, blank=True)
    process = models.CharField(max_length=100, null=True, blank=True)
    user_ip = models.CharField(max_length=100, null=True, blank=True)
    activity_desc = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        app_label = 'djams'

class ADM_HelpPage(models.Model):
    '''
    Description: App specific help descriptions are written and stored in this model. This way, apps can have their help updated on the fly in a production environment.  
    '''

    name = models.CharField(max_length=200, null=False, blank=False)
    narrative = models.CharField(max_length=4000, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:helppage-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:helppage-del', arg[str(self.id)])

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'djams'


class ADM_UserSession(models.Model):
    '''
    Description: Admin model to record user sessions. Required for multi-microsites
    '''

    user = models.ForeignKey(ADM_CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        app_label = 'djams'

class ADM_UserProfile(models.Model):

    '''
    Description: Admin model to record user profile information.
    '''
    user = models.OneToOneField(ADM_CustomUser, on_delete=models.CASCADE)
    employer = models.ForeignKey(MDS_Company, related_name='user_employer', on_delete=models.SET_NULL, null=True, blank=True)
    employerco = models.ForeignKey(MDS_Company, related_name="employer_company", on_delete=models.SET_NULL, null=True, blank=True)
    resident_country = models.ForeignKey(MDS_Country, related_name="user_country", on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, default='user_thumbnails/default.jpg')

    creation_date = models.DateField(auto_now_add=True, blank=True)
    creation_user = models.ForeignKey(ADM_CustomUser, related_name="user_creator", on_delete=models.SET_NULL, null=True, blank=True)
    last_update_date = models.DateField(auto_now=True, blank=True)
    last_update_user = models.ForeignKey(ADM_CustomUser, related_name='user_updater', on_delete=models.SET_NULL, null=True, blank=True)

    require_password_reset = models.BooleanField(default='False')
    invalid_login_attempts = models.IntegerField(default=0, null=True, blank=True)
    password_change_date = models.DateField(null=True, blank=True)

    pp1 = models.TextField(max_length=128, null=True, blank=True)
    ps1 = models.TextField(max_length=128, null=True, blank=True)
    pp2 = models.TextField(max_length=128, null=True, blank=True)
    ps2 = models.TextField(max_length=128, null=True, blank=True)
    pp3 = models.TextField(max_length=128, null=True, blank=True)
    ps3 = models.TextField(max_length=128, null=True, blank=True)
    pp4 = models.TextField(max_length=128, null=True, blank=True)
    ps4 = models.TextField(max_length=128, null=True, blank=True)
    pp5 = models.TextField(max_length=128, null=True, blank=True)
    ps5 = models.TextField(max_length=128, null=True, blank=True)
    pp6 = models.TextField(max_length=128, null=True, blank=True)
    ps6 = models.TextField(max_length=128, null=True, blank=True)
    pp7 = models.TextField(max_length=128, null=True, blank=True)
    ps7 = models.TextField(max_length=128, null=True, blank=True)
    pp8 = models.TextField(max_length=128, null=True, blank=True)
    ps8 = models.TextField(max_length=128, null=True, blank=True)
    pp9 = models.TextField(max_length=128, null=True, blank=True)
    ps9 = models.TextField(max_length=128, null=True, blank=True)
    pp10 = models.TextField(max_length=128, null=True, blank=True)
    ps10 = models.TextField(max_length=128, null=True, blank=True)

    pp11 = models.TextField(max_length=128, null=True, blank=True)
    ps11 = models.TextField(max_length=128, null=True, blank=True)
    pp12 = models.TextField(max_length=128, null=True, blank=True)
    ps12 = models.TextField(max_length=128, null=True, blank=True)
    pp13 = models.TextField(max_length=128, null=True, blank=True)
    ps13 = models.TextField(max_length=128, null=True, blank=True)
    pp14 = models.TextField(max_length=128, null=True, blank=True)
    ps14 = models.TextField(max_length=128, null=True, blank=True)
    pp15 = models.TextField(max_length=128, null=True, blank=True)
    ps15 = models.TextField(max_length=128, null=True, blank=True)
    pp16 = models.TextField(max_length=128, null=True, blank=True)
    ps16 = models.TextField(max_length=128, null=True, blank=True)
    pp17 = models.TextField(max_length=128, null=True, blank=True)
    ps17 = models.TextField(max_length=128, null=True, blank=True)
    pp18 = models.TextField(max_length=128, null=True, blank=True)
    ps18 = models.TextField(max_length=128, null=True, blank=True)
    pp19 = models.TextField(max_length=128, null=True, blank=True)
    ps19 = models.TextField(max_length=128, null=True, blank=True)
    pp20 = models.TextField(max_length=128, null=True, blank=True)
    ps20 = models.TextField(max_length=128, null=True, blank=True)

    pp21 = models.TextField(max_length=128, null=True, blank=True)
    ps21 = models.TextField(max_length=128, null=True, blank=True)
    pp22 = models.TextField(max_length=128, null=True, blank=True)
    ps22 = models.TextField(max_length=128, null=True, blank=True)
    pp23 = models.TextField(max_length=128, null=True, blank=True)
    ps23 = models.TextField(max_length=128, null=True, blank=True)

    def get_absolute_url_edit(self):
        return reverse('admin_portal:user-edit', arg[str(self.id)])

    def get_absolute_url_del(self):
        return reverse('admin_portal:user-del', arg[str(self.user.id)])

    def __str__(self):
        return str(self.user.username)

    class Meta:
        app_label = 'djams'

@receiver(post_save, sender=ADM_CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ADM_UserProfile.objects.create(user=instance)

@receiver(post_save, sender=ADM_CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.adm_userprofile.save()

class ADM_App_Data_Dest(models.Model):
    '''
    Description: Records the destination for source data for ingestion straight in to an app relevant model 
    '''
    app = models.ForeignKey(ADM_App, related_name='app_data_desc_to_app', null=True, on_delete=models.SET_NULL)
    folder_identifier = models.CharField(max_length=200, null=True, blank=True) # each app could have multiple file types and these should be separated by folders, hence this field
    file_descriptor = models.CharField(max_length=200, null=True, blank=True) # each app could have multiple file types. Descriptor used to differentiate
    relevant_model = models.CharField(max_length=200, null=False, blank=False) # the lower case version of the table name in database
    use_django_app_model_prefix = models.BooleanField(default=True, null=False, blank=False)
    custom_upload_query = models.CharField(max_length=1000, null=True, blank=True) # used if trying to load e.g. a .dat file using custom query

    def __str__(self):
        return "%s  /  %s  /  %s" %(str(self.app.django_app_name), str(self.folder_identifier), str(self.relevant_model))

    class Meta:
        app_label = 'djams'

class RDS_Company_Data_Ingest_Meta(models.Model):
    '''
    Description: Records historical automatic data ingestion actions
    '''
    file_name = models.CharField(max_length=255, null=True, blank=True)
    #data_desc = models.ForeignKey(ADM_App_Data_Desc, related_name='rds_company_data_ingest_meta_to_app_app_data_desc', null=True, on_delete=models.SET_NULL)
    upload_user = models.CharField(max_length=100, null=True, blank=True)
    upload_username = models.CharField(max_length=100, null=True, blank=True)
    client = models.CharField(max_length=200, null=True, blank=True)
    django_app_name = models.CharField(max_length=150, null=True, blank=True)
    event_datetime = models.DateTimeField(null=True, blank=True)
    event_result = models.CharField(max_length=100, null=True, blank=True)
    activity_desc = models.CharField(max_length=300, null=True, blank=True)

    # class Meta:
    #     app_label = 'djams'
