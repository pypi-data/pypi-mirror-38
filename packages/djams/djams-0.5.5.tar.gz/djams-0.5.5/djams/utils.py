import datetime
from django.core.paginator import Paginator
from .models import ADM_AppSessionAudit, ADM_App
from .config_vars import APP_PORTALS


def refineFilterQuery(queryDict):
    '''
    Description: This is used to refine Django view filters in order to remove parameter values such as 'ALL' or blank values, which would suggest that the user wants all available info
    Inputs: queryDict - a dictionary containing parameter keys and the user set values from dropdowns.
    Returns: a filtered dictionary which can be used in a call to a database object 
    '''
    # filter out "ALL" values:
    filtered = {}
    queryDict = {i:queryDict[i] for i in queryDict if 'ALL' not in queryDict[i]}
    
    # filter out blank values in lists:
    for i in queryDict:
        value = queryDict[i]
        if isinstance(value, list) != True and 'All' not in value and value != '':
            filtered[i] = value
        elif isinstance(queryDict[i], list):
            if '' not in value:
                filtered[i] = value
    
    return filtered

def obtainForeignKeyObjects(queryDict, model):
    '''
    Description:
    Inputs: queryDict - a django models query dictionary.
            model - a standard Django model with a foreign key
    Returns: a dictionary containing the object versions of the foreign keys to be filtered on
    N.B. on models: This funciton assumes that the primary key of the foreign kety models renamed 'id
    '''

    for field in model._meta.fields:
        if field.get_internal_type() == 'ForeignKey' and field.name in list(queryDict.keys()):
            print("Found a foreign key. Getting object: " + field.name)
            temp = {}
            temp['id'] = queryDict[field.name]
            print(str(temp))
            foreign_model = model._meta.get_field(field.name).remote_field.model
            print("Foreign model is: %s" %(str(foreign_model)))
            foreign_object_list = foreign_model.objects.filter(**temp)
            if len(foreign_object_list) > 0:
                queryDict[field.name] = foreign_object_list[0]
    
    return queryDict

def getSetAppInfo(request):
    '''
    Description: Sets the current app name in the request.session object 
    '''
    main_app = request.request_apps[0]
    main_app_name = main_app.split('.')[0]
    print("The main app name is: %s" %(main_app_name))

    # SERVER_ENV = settings.SERVER_ENV

    if main_app_name in APP_PORTALS:
        request.session['myappname'] = main_app_name

    else:
        sessionapp = ADM_App.objects.get(django_app_name=main_app_name)
        print("getSetAppInfo: current session app is: %s" %(str(sessionapp)))
        request.session['myapp'] = sessionapp.id
        request.session['myappname'] = sessionapp.name

    return

def paginate_pages(request, page_list, page_entries=10):

    page = request.GET.get('page', 1)
    paginator = Paginator(page_list, page_entries)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    
    return page, paginator, messages

def update_creation_fields(form_inst, user):
    form_inst.creation_user = user
    form_inst.creation_date = datetime.datetime.today().strftime("%Y-%m-%d")
    return form_inst

def update_last_update_fields(form_inst, user):
    form_inst.last_update_user = user
    form_inst.last_update_date = datetime.datetime.today().strftime("%Y-%m-%d")
    return form_inst

def auditlog(request, viewname, action, result, username='', subjectuser='', subjectusername='', client=None):
    '''
    Description: Used for auditing user actions such as microsite logging in and logging out
    '''

    auditrecord = ADM_AppSessionAudit.objects.create()
    try:
        auditrecord.token = request.session['appsession']
    except:
        auditrecord.token = None

    try:
        auditrecord.user = request.user
    except:
        auditrecord.user = None
    
    if username is not "":
        auditrecord.username = username

    else:
        auditrecord.username = request.user.username

    auditrecord.client = client

    request_apps = request.request_apps

    getSetAppInfo(request)
    auditrecord.appname = request.session['myappname']

    auditrecord.app = None
    auditrecord.eventitme = datetime.datetime.now()

    auditrecord.eventresult = result
    if subjectuser is not None:
        auditrecord.subjectuser = subjectuser
    auditrecord.subjectusername = subjectusername
    auditrecord.process = viewname
    auditrecord.userip = '0.0.0.0'
    x_forwarded_for = request.META.get('REMOTE_ADDR')
    auditrecord.description = action
    auditrecord.save()
    print("Audit record saved.")

    return ('ADM_AppSessionAudit audit log written')