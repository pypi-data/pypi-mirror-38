from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.core.paginator import Paginator
from django.db.models import Max
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import datetime
from datetime import timedelta
import dateutil.parser
import hashlib
from django.http import HttpResponseRedirect, HttpResponse


from .models import *
from .djams_forms import *
from .config_vars import SUPERUSER_APPS, APP_PORTALS
# from .djams_model_views import *

def reset_to_baseurl(request):
    return HttpResponseRedirect('')

@login_required
def launch_app(request):
    '''
    Description: this is the intitla view used when the app is first launched
    '''
    return redirect('djams:appsession')

def djams_home_page(request):
    '''
    Description: This is a link to the main home page of the app portal
    '''
    return redirect('https://www.burmicz.com')


def djams_privacy_notice(request):
    '''
    Description: Privacy notice for the app portal
    '''
    return render(request, 'djams/djams_privacy_notice.html')

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

def getCurrentClientInfo(request, context):
    '''
    Description: Gets the name of the current client using the session context in request.
        Returns: A "context" dict. This will either contain info on the current client or nothing if no client has been selected 
    '''

    try:
        myclient = MDS_Company.objects.get(id=request.sesssion['myclient'])
        context['myclient'] = myclient.registered_name
        context['myclientid'] = myclient.id
        return context
    except KeyError as ke:
        print("getCurrentClientInfo: No client currently selected.")
        return context

def getCurrentAppInfo(request, context):
    '''
    Description: Gets the name of the app in the microsite using the session context in request
        Returns: A "context" dictionary. This is left untouched if no app selected.
    '''
    try:
        getSetAppInfo(request)
        myapp = request.session['myapp']
        myapprecord = ADM_App.objects.get(id=myapp)
        context['myapp'] = myapprecord.name
        context['myappid'] = myapprecord.id
        return context
    except KeyError as ke:
        print("getCurrentAppInfo: No app currently selected.")
        return context


def getAllClients(request, context):
    '''
    Description: Gets a list of clients using the session context in request
        Returns: a context dictionary with a list of clients or it is left untouched if no clients available to use user
    '''

    try:
        context['clients'] = UserClients_View.objects.filter(user_id=request.user.id).filter(app_id=request.session['myapp'])
        return context
    except KeyError as ke:
        print("getAllClients: No app currently selected or no clients available to view")
        return context

def getUserAppClientInfo(request):
    '''
    Description: Gets info relating to the current App and Client combination for use in a template. E.g. it can be used fopr populating a sidebar with the name of the current app and client in use 
                 for the current session
    '''
    context = {}
    context = getAllClients(request, context)
    context = getCurrentClientInfo(request, context)
    context = getCurrentAppInfo(request, context)
    context['userid'] = request.user.id
    return context


@login_required
def my_clients(request):
    '''
    Description: This function shows a list of clients available to the user. This is required before retrieving any solid data for your app since the data will be client specific.
    '''

    context = getUserAppClientInfo(request)
    context = getAllClients(request, context)
    main_app_name = request.request_apps[0].split('.')[0]

    return render(request, 'djams/myclients.html', context=context)


@login_required
def client_select(request):
    '''
    Description: This function is necessary for multi-client apps requiring database separation at the client level. This function is called after the user has selected from a list of clients available to them.
                It then sets the avaialble sub client databases in the request.session object, which is used for routing object requests
                '''

    # retrieve the current session record from the database:
    sessionuser = request.user.id
    appsession = ADM_AppSession.objects.get(user_id=sessionuser)
    sessiontoken = appsession.token
    sessiontime = dateime.dateime.now()
    sessionclient = pk

    # get the app id based on the current apps django_app_name:
    main_app_name = settings.AUTHORIZED_APPS[0].split('.')[0]
    current_app = ADM_App.objects.get(django_app_name=main_app_name)

    appsession.client_id = sessionclient
    appsesssion.logintime = sessiontime
    appsession.save()

    # copy the session data to the session audit log:
    sessionaudit = ADM_AppSessionAudit.objects.create(token=appsession.token, user_id=request.user.id, client_id=sessionclient, app_id=current_app.id, eventtime=sessiontime)
    sessionaudit.save()

    # set session vartiables for the app to make iti easy for app developer to get basic information
    company = MDS_Company.objects.get(id=sessionclient)
    current_database = str(company.database)

    request.session['myclient'] = sessionclient
    request.session['myclientname'] = MDS_Company.registered_name
    request.session['myapp'] = current_app.id
    request.session['myappname'] = current_app.name
    request.session['rds'] = "RDS_" + current_database
    request.session['tds'] = "TDS_" + current_database
    request.session['ads'] = "ADS_" + current_database

    dash_context = request.session.get('django_plotly_dash', dict())
    dash_context['rds'] = request.session['rds']
    dash_context['tds'] = request.session['tds']
    dash_context['ads'] = request.session['ads']
    request.session['django_plotly_dash'] = dash_context

    print("Printing client specific info:\n%s\n%s\n%s\n%s\n%s" %(request.session['myclientname'], request.session['myappname'], request.session['rds'], request.session['tds'], request.session['ads']))    

    try:
        myrolerecord = ADM_UserAppRole.objects.get(user=request.user.id, app=sessionapp.id)
        request.session['myrole'] = myrolerecord.role.name
    except:
        request.session['myrole'] = "Level 1 App User"
     
    return redirect('%s:app-home-page' %(main_app_name))

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

def signUserIn(request, user, username):

    '''
    Description: Signing the user in if initial authentication was successful
    '''

    print("signUserIn: Logging user in")
    
    request.session['user_request_page'] = request.path

    login(request, user)
    user.adm_userprofile.invalid_login_attempts = 0
    user.save()

    if not request.session.exists(request.session.session_key):
        request.session.create() 

    # create user session
    instance = ADM_UserSession.objects.create(user=request.user, session_id=request.session.session_key)
    instance.save()
    # write audit record
    action = 'User successfully logged in to %s' %(str(request.request_apps))
    result = "Success"
    print("signUserIn: create audit log entry")
    auditlog(request, viewname="signin", action=action, result=result, username=request.user.username,
             subjectuser=None, subjectusername='', client=None)

    # find and deete any sessions using the same user's credentials
    usersessions = ADM_UserSession.objects.filter(user_id=request.user.id).exclude(session_id=request.session.session_key).values()
    for session in usersessions:
        ustodelete = ADM_UserSession.objects.filter(session_id=session['session_id'])
        ustodelete.delete()
        roguesession = Session.objects.filter(session_key=session['session_id'])
        roguesession.delete()
    print("signUserin: Sign in complete")
    return

def dontSignUserIn(request, user, username):
    '''
    Description: If authentication was unsuccessful, this function is called and logs the failure
    '''

    auditrecord = ADM_AppSessionAudit.objects.create()
    action = "Unsuccessful attempt to log in to %s" %(str(request.request_apps))
    result = 'Fail'
    auditlog(request, "signin", action, result, username, None, '')
    try:
        asserteduser = ADM_CustomUserobjects.filter(username=username).first()
        loginattempt = int(asserteduser.adm_userprofile.invalid_login_attempts) + 1
        print("dontSignUserIn: Login attempts so far: %s" %(loginattempts))
        asserteduser.adm_userprofile.invalid_login_attempts = loginattempts
        if loginattempts > 5:
            print("dontSignUserIn: loginattempts > 5. Setting user as no longer active")
            asserteduser.is_active = 0
        asserteduser.save()
    except:
        pass
    return

def apps_require_superuser_check(request_apps):
    '''
    Description: Checks the list of current apps being used as part of the app against the list in the SUPERUSERAPPS variable
    '''
    for request_app in request_apps:
        if any(super_app in request_app for super_app in SUPERUSER_APPS):
            return True
    return False

def signin(request):
    '''
    Description: The main custom signin function for authenticating users. The 'signUserIn' or 'dontSignUserin' functions are called \
                 depending on whether the user has been authenticated or not. All actions are recorded via the auditlog function 
    '''

    request_apps = request.request_apps
    main_request_app = request_apps[0].split('.')[0]

    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = request.POST['username']
        print(username)

        password = request.POST['password']
        #print(password)
        user = authenticate(request, username=username, password=password)
        print("signIn: User authenticated object: %s" %(user))
        print("signIn: request_apps: %s" %(str(request_apps)))

        if request.use_microsite_auth:
            superuser_required = apps_require_superuser_check(request_apps)
        
        # elif request.admin:
        #     print("setting superuser_required (reason: request.admin)")
        #     superuser_required = True
        else:
            superuser_required = False
     
        if superuser_required:
        
            print("signin: This site requires superuser privelages. Checking if user holds priveleges")
            if user is not None:
                if user.is_staff is True:
                    print("signin: User is member of staff. Running 'signUserIn.")
                    signUserIn(request, user, username)
                    return redirect('djams:appsession')
                else:
                    print("User field is None")
                    return redirect('djams:noaccess')
            
            else:
                print("signin: User is not member of staff. Running 'dontSignUserIn'")
                dontSignUserIn(request, user, username)
                return redirect('djams:noaccess')
        
        else:
            print("signin: The apps used for this microsite do not require superuser privelages. ")

            if user is not None:
                print("signin: user field is not blank. starting SignUserIn.")
                signUserIn(request, user, username)
                return redirect('djams:appsession')
            
            else:
                print("signin: User field was received as 'None'. Not signing user in.")
                dontSignUserIn(request, user, username)
                return redirect('djams:login')
    
    else:
        print("signin: Producing a fresh user login form.")
        form = LoginForm(request.POST)

    return render(request, 'djams/login.html', {'form':form, 'main_request_app':main_request_app})

@login_required
def appsession(request):
    '''
    Description: Creates objects of AppSession denoting the start and end of an app session
    '''
    print("appsession. Setting session info.")
    sessionuser = request.user.id
    sessiontoken = str(uuid.uuid4())
    request.session['appsession'] = str(sessiontoken)
    sessiontime = datetime.datetime.now()
    main_app_name = request.request_apps[0].split('.')[0]

    # create an app session for the platform user:

    action = deleteAppSessionObj(request, sessionuser)

    newSession = ADM_AppSession.objects.create(user_id=sessionuser)
    newSession.save()

    result = 'Success'
    
    auditlog(request, viewname="appsession", action=action, result=result, username=request.user.username,
             subjectuser=None, subjectusername='', client=None)

    # copy the session data to the session audit log to store the app portals session cookie
    currentdate = dateutil.parser.parse(str(datetime.datetime.now())).date()
    asserteduser = ADM_CustomUser.objects.get(id=sessionuser)

    print("appsession: Running password history checks..")

    if asserteduser.adm_userprofile.password_change_date is None:
        print("appsession: User %s has never changed password" %(asserteduser))

        if asserteduser.is_staff == 1:
            days_upper_limit = 44
        else:
            days_upper_limit = 85

        asserteduser.adm_userprofile.password_change_date = currentdate - timedelta(days=days_upper_limit)
        print("appsession: password age: %s" %(asserteduser.adm_userprofile.password_change_date))
        asserteduser.save()

    days_since_pw_change = (currentdate - asserteduser.adm_userprofile.password_change_date).days

    if asserteduser.is_staff == 1:
        print("appsession: User is a staff member")

        if 40 < days_since_pw_change <= 45:
            return redirect('djams:change-password')
        
        elif days_since_pw_change > 45:
            asserteduser.is_active = 0
            asserteduser.save()
            return redirect('djams:logout')
    
    else:
        print("appsession: User is not a staff member")

        if 85 <= days_since_pw_change <= 90:
            return redirect('djams:change-password')
        
        elif days_since_pw_change > 90:
            asserteduser.is_active = 0
            asserteduser.save()
            return redirect('djams:logout')
        else:
            
            
            next_url = request.POST.get('next')
            print(request.POST)
            print(request.GET)

            if next_url:
                print("redirecting to next: %s" %(next_url))
                return HttpResponseRedirect(next_url)
            
            user_request_url = request.session.get('user_request_page', False)

            if user_request_url:
                user_request_url = str(user_request_url).replace('login/', '')
                print("user_Request_url: %s" %(user_request_url))
                return redirect(user_request_url)

            return redirect(main_app_name+':app-home-page')
    
    next_url = request.POST.get('next')
    if next_url:
        print("redirecting to next: %s" %(next_url))
        return HttpResponseRedirect(next_url)
    
    user_request_url = request.session.get('user_request_page', False)

    if user_request_url:
        user_request_url = str(user_request_url).replace('login/', '')
        print("user_Request_url: %s" %(user_request_url))
        return redirect(user_request_url)

    return redirect(main_app_name+':app-home-page')

def deleteAppSessionObj(request, sessionuser):

    if ADM_AppSession.objects.filter(user_id=sessionuser).exists():
        ADM_AppSession.objects.filter(user_id=sessionuser).delete()
        action = 'Old session token deleted and new one created'
    else:
        action = 'No old session to delete. New one created'

    return action

def logout_redirect(request):

    logout(request)

    return redirect('/')


@login_required
def endappsession(request):
    '''
    Description: Ends an app session
    '''
    sessionuser = request.user.id
    sessionusername = request.user.username
    sessiontoken = str(uuid.uuid4())
    sessiontime = datetime.datetime
    application_name = request.request_apps[0].split('.')[0]
    #request.session['app_redirect_name'] = application_name
    print("endappsession: Application name: %s" %(application_name))

    sessionprocess = 'Logout / End App Session'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        sessionuserip = x_forwarded_for.split(',')[0]
    else:
        sessionuserip = request.META.get('REMOTE_ADDR')

    usersessions = ADM_UserSession.objects.filter(user_id=request.user.id).values()
    for session in usersessions:
        ustodelete = ADM_UserSession.objects.filter(session_id=session['session_id'])
        ustodelete.delete()


    action = deleteAppSessionObj(request, sessionuser)

    newSession = ADM_AppSession.objects.create(user_id=sessionuser)
    newSession.save()

    result = 'Success'
    
    auditlog(request, viewname="endappsession", action=action, result=result, username=request.user.username,
             subjectuser=None, subjectusername='', client=None)

    # return redirect('/')
    return redirect('djams:userlogout')

def check_redirect_page(request):

    BAN_REDIRECT_POST_LOGIN = ['login', 'change_password']

    for i in BAN_REDIRECT_POST_LOGIN:
        if i in request.session['user_request_page']:
            request.session['user_request_page'] = '/'
    return


@login_required
def change_password(request):

    print("user requested page: %s" %(str(request.session['user_request_page'])))

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        newpassword = request.POST['new_password1']
        asserteduser = ADM_CustomUser.objects.get(id=request.user.id)
        pp1 = asserteduser.adm_userprofile.pp1
        ps1 = asserteduser.adm_userprofile.ps1
        pp2 = asserteduser.adm_userprofile.pp2
        ps2 = asserteduser.adm_userprofile.ps2
        pp3 = asserteduser.adm_userprofile.pp3
        ps3 = asserteduser.adm_userprofile.ps3
        ####### ADDITION OTHER 20 PASSWORDS #####
        pp4 = asserteduser.adm_userprofile.pp4
        ps4 = asserteduser.adm_userprofile.ps4
        pp5 = asserteduser.adm_userprofile.pp5
        ps5 = asserteduser.adm_userprofile.ps5
        pp6 = asserteduser.adm_userprofile.pp6
        ps6 = asserteduser.adm_userprofile.ps6
        pp7 = asserteduser.adm_userprofile.pp7
        ps7 = asserteduser.adm_userprofile.ps7
        pp8 = asserteduser.adm_userprofile.pp8
        ps8 = asserteduser.adm_userprofile.ps8
        pp9 = asserteduser.adm_userprofile.pp9
        ps9 = asserteduser.adm_userprofile.ps9
        pp10 = asserteduser.adm_userprofile.pp10
        ps10 = asserteduser.adm_userprofile.ps10
        pp11 = asserteduser.adm_userprofile.pp11
        ps11 = asserteduser.adm_userprofile.ps11
        pp12 = asserteduser.adm_userprofile.pp12
        ps12 = asserteduser.adm_userprofile.ps12
        pp13 = asserteduser.adm_userprofile.pp13
        ps13 = asserteduser.adm_userprofile.ps13
        pp14 = asserteduser.adm_userprofile.pp14
        ps14 = asserteduser.adm_userprofile.ps14
        pp15 = asserteduser.adm_userprofile.pp15
        ps15 = asserteduser.adm_userprofile.ps15
        pp16 = asserteduser.adm_userprofile.pp16
        ps16 = asserteduser.adm_userprofile.ps16
        pp17 = asserteduser.adm_userprofile.pp17
        ps17 = asserteduser.adm_userprofile.ps17
        pp18 = asserteduser.adm_userprofile.pp18
        ps18 = asserteduser.adm_userprofile.ps18
        pp19 = asserteduser.adm_userprofile.pp19
        ps19 = asserteduser.adm_userprofile.ps19
        pp20 = asserteduser.adm_userprofile.pp20
        ps20 = asserteduser.adm_userprofile.ps20
        pp21 = asserteduser.adm_userprofile.pp21
        ps21 = asserteduser.adm_userprofile.ps21
        pp22 = asserteduser.adm_userprofile.pp22
        ps22 = asserteduser.adm_userprofile.ps22
        pp23 = asserteduser.adm_userprofile.pp23
        ps23 = asserteduser.adm_userprofile.ps23
        ###### END OF ADDITION 20 MORE PASSWORDS ####


        if pp1 is not None and ps1 is not None:
            hashpass1 = hashlib.sha256(ps1.encode() + newpassword.encode()).hexdigest() + ':' + ps1
        if pp2 is not None and ps2 is not None:
            hashpass2 = hashlib.sha256(ps2.encode() + newpassword.encode()).hexdigest() + ':' + ps2
        if pp3 is not None and ps3 is not None:
            hashpass3 = hashlib.sha256(ps3.encode() + newpassword.encode()).hexdigest() + ':' + ps3
        ####### ADDITION OTHER 20 PASSWORDS ######
        if pp4 is not None and ps4 is not None:
            hashpass4 = hashlib.sha256(ps4.encode() + newpassword.encode()).hexdigest() + ':' + ps4
        if pp5 is not None and ps5 is not None:
            hashpass5 = hashlib.sha256(ps5.encode() + newpassword.encode()).hexdigest() + ':' + ps5
        if pp6 is not None and ps6 is not None:
            hashpass6 = hashlib.sha256(ps6.encode() + newpassword.encode()).hexdigest() + ':' + ps6
        if pp7 is not None and ps7 is not None:
            hashpass7 = hashlib.sha256(ps7.encode() + newpassword.encode()).hexdigest() + ':' + ps7
        if pp8 is not None and ps8 is not None:
            hashpass8 = hashlib.sha256(ps8.encode() + newpassword.encode()).hexdigest() + ':' + ps8
        if pp9 is not None and ps9 is not None:
            hashpass9 = hashlib.sha256(ps9.encode() + newpassword.encode()).hexdigest() + ':' + ps9
        if pp10 is not None and ps10 is not None:
            hashpass10 = hashlib.sha256(ps10.encode() + newpassword.encode()).hexdigest() + ':' + ps10
        if pp11 is not None and ps11 is not None:
            hashpass11 = hashlib.sha256(ps11.encode() + newpassword.encode()).hexdigest() + ':' + ps11
        if pp12 is not None and ps12 is not None:
            hashpass12 = hashlib.sha256(ps12.encode() + newpassword.encode()).hexdigest() + ':' + ps12
        if pp13 is not None and ps13 is not None:
            hashpass13 = hashlib.sha256(ps13.encode() + newpassword.encode()).hexdigest() + ':' + ps13
        if pp14 is not None and ps14 is not None:
            hashpass14 = hashlib.sha256(ps14.encode() + newpassword.encode()).hexdigest() + ':' + ps14
        if pp15 is not None and ps14 is not None:
            hashpass15 = hashlib.sha256(ps15.encode() + newpassword.encode()).hexdigest() + ':' + ps15
        if pp16 is not None and ps16 is not None:
            hashpass16 = hashlib.sha256(ps16.encode() + newpassword.encode()).hexdigest() + ':' + ps16
        if pp17 is not None and ps17 is not None:
            hashpass17 = hashlib.sha256(ps17.encode() + newpassword.encode()).hexdigest() + ':' + ps17
        if pp18 is not None and ps18 is not None:
            hashpass18 = hashlib.sha256(ps18.encode() + newpassword.encode()).hexdigest() + ':' + ps18
        if pp19 is not None and ps19 is not None:
            hashpass19 = hashlib.sha256(ps19.encode() + newpassword.encode()).hexdigest() + ':' + ps19
        if pp20 is not None and ps20 is not None:
            hashpass20 = hashlib.sha256(ps20.encode() + newpassword.encode()).hexdigest() + ':' + ps20
        if pp21 is not None and ps21 is not None:
            hashpass21 = hashlib.sha256(ps21.encode() + newpassword.encode()).hexdigest() + ':' + ps21
        if pp22 is not None and ps22 is not None:
            hashpass22 = hashlib.sha256(ps22.encode() + newpassword.encode()).hexdigest() + ':' + ps22
        if pp23 is not None and ps23 is not None:
            hashpass23 = hashlib.sha256(ps23.encode() + newpassword.encode()).hexdigest() + ':' + ps23
        ###### END OF ADDITION 20 MORE PASSWORDS ####

        duplicatepass = False

        if pp1 is None:
            pass
        elif pp1 == hashpass1:
            duplicatepass = True
        if pp2 is None:
            pass
        elif pp2 == hashpass2:
            duplicatepass = True
        if pp3 is None:
            pass
        elif pp3 == hashpass3:
            duplicatepass = True
        ####### ADDITION OTHER 20 PASSWORDS #####
        if pp4 is None:
            pass
        elif pp4 == hashpass4:
            duplicatepass = True
        if pp5 is None:
            pass
        elif pp5 == hashpass5:
            duplicatepass = True
        if pp6 is None:
            pass
        elif pp6 == hashpass6:
            duplicatepass = True
        if pp7 is None:
            pass
        elif pp7 == hashpass7:
            duplicatepass = True
        if pp8 is None:
            pass
        elif pp8 == hashpass8:
            duplicatepass = True
        if pp9 is None:
            pass
        elif pp9 == hashpass9:
            duplicatepass = True
        if pp10 is None:
            pass
        elif pp10 == hashpass10:
            duplicatepass = True
        if pp11 is None:
            pass
        elif pp11 == hashpass11:
            duplicatepass = True
        if pp12 is None:
            pass
        elif pp12 == hashpass12:
            duplicatepass = True
        if pp13 is None:
            pass
        elif pp13 == hashpass13:
            duplicatepass = True
        if pp14 is None:
            pass
        elif pp14 == hashpass14:
            duplicatepass = True
        if pp15 is None:
            pass
        elif pp15 == hashpass15:
            duplicatepass = True
        if pp16 is None:
            pass
        elif pp16 == hashpass16:
            duplicatepass = True
        if pp17 is None:
            pass
        elif pp17 == hashpass17:
            duplicatepass = True
        if pp18 is None:
            pass
        elif pp18 == hashpass18:
            duplicatepass = True
        if pp19 is None:
            pass
        elif pp19 == hashpass19:
            duplicatepass = True
        if pp20 is None:
            pass
        elif pp20 == hashpass20:
            duplicatepass = True
        if pp21 is None:
            pass
        elif pp21 == hashpass21:
            duplicatepass = True
        if pp22 is None:
            pass
        elif pp22 == hashpass22:
            duplicatepass = True
        if pp23 is None:
            pass
        elif pp23 == hashpass23:
            duplicatepass = True
        ###### END OF ADDITION 20 OTHER PASSWORDS #####


        if newpassword == request.POST['old_password']:
            duplicatepass = True
        if duplicatepass == True:
            form.add_error('new_password1', "Password must be different to current password and past 23 passwords")
        if not any(x.isupper() for x in newpassword):
            form.add_error('new_password1', "Passwords must contain at least one capital letter")
        if not any(x.islower() for x in newpassword):
            form.add_error('new_password1', "Passwords must contain at least one lower case letter")
        if not any(x.isdigit() for x in newpassword):
            form.add_error('new_password1', "Passwords must contain at least one digit")
        if len(newpassword) < 10:
            form.add_error('new_password1', "Passwords must contain at least ten characters")

        if form.is_valid():
            user = form.save()
            user.adm_userprofile.password_change_date = datetime.datetime.now()
            pp1 = user.adm_userprofile.pp1
            ps1 = user.adm_userprofile.ps1
            pp2 = user.adm_userprofile.pp2
            ps2 = user.adm_userprofile.ps2
            pp3 = user.adm_userprofile.pp3
            ps3 = user.adm_userprofile.ps3
            #### ADD 20 PASSWORDS ####
            pp4 = user.adm_userprofile.pp4
            ps4 = user.adm_userprofile.ps4
            pp5 = user.adm_userprofile.pp5
            ps5 = user.adm_userprofile.ps5
            ps6 = user.adm_userprofile.ps6
            pp6 = user.adm_userprofile.pp6
            ps7 = user.adm_userprofile.ps7
            pp7 = user.adm_userprofile.pp7
            ps8 = user.adm_userprofile.ps8
            pp8 = user.adm_userprofile.pp8
            ps9 = user.adm_userprofile.ps9
            pp9 = user.adm_userprofile.pp9
            ps10 = user.adm_userprofile.ps10
            pp10 = user.adm_userprofile.pp10
            ps11 = user.adm_userprofile.ps11
            pp11 = user.adm_userprofile.pp11
            ps12 = user.adm_userprofile.ps12
            pp12 = user.adm_userprofile.pp12
            ps13 = user.adm_userprofile.ps13
            pp13 = user.adm_userprofile.pp13
            pp14 = user.adm_userprofile.pp14
            ps14 = user.adm_userprofile.ps14
            pp15 = user.adm_userprofile.pp15
            ps15 = user.adm_userprofile.ps15
            pp16 = user.adm_userprofile.pp16
            ps16 = user.adm_userprofile.ps16
            pp17 = user.adm_userprofile.pp17
            ps17 = user.adm_userprofile.ps17
            pp18 = user.adm_userprofile.pp18
            ps18 = user.adm_userprofile.ps18
            pp19 = user.adm_userprofile.pp19
            ps19 = user.adm_userprofile.ps19
            pp20 = user.adm_userprofile.pp20
            ps20 = user.adm_userprofile.ps20
            pp21 = user.adm_userprofile.pp21
            ps21 = user.adm_userprofile.ps21
            pp22 = user.adm_userprofile.pp22
            ps22 = user.adm_userprofile.ps22
            pp23 = user.adm_userprofile.pp23
            ps23 = user.adm_userprofile.ps23
            ### END OF ADD 20 PASSWORDS ###

            salt = uuid.uuid4().hex
            password = request.POST['old_password']
            user.adm_userprofile.pp1 = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
            user.adm_userprofile.ps1 = salt
            user.adm_userprofile.pp2 = pp1
            user.adm_userprofile.ps2 = ps1
            user.adm_userprofile.pp3 = pp2
            user.adm_userprofile.ps3 = ps2
            ### ADD 20 NEW PASSWORDS ###
            user.adm_userprofile.pp4 = pp3
            user.adm_userprofile.ps4 = ps3
            user.adm_userprofile.pp5 = pp4
            user.adm_userprofile.ps5 = ps4
            user.adm_userprofile.pp6 = pp5
            user.adm_userprofile.ps6 = ps5
            user.adm_userprofile.pp7 = pp6
            user.adm_userprofile.ps7 = ps6
            user.adm_userprofile.pp8 = pp7
            user.adm_userprofile.ps8 = ps7
            user.adm_userprofile.pp9 = pp8
            user.adm_userprofile.ps9 = ps8
            user.adm_userprofile.pp10 = pp9
            user.adm_userprofile.ps10 = ps9
            user.adm_userprofile.pp11 = pp10
            user.adm_userprofile.ps11 = ps10
            user.adm_userprofile.pp12 = pp11
            user.adm_userprofile.ps12 = ps11
            user.adm_userprofile.pp13 = pp12
            user.adm_userprofile.ps13 = ps12
            user.adm_userprofile.pp14 = pp13
            user.adm_userprofile.ps14 = ps13
            user.adm_userprofile.pp15 = pp14
            user.adm_userprofile.ps15 = ps14
            user.adm_userprofile.pp16 = pp15
            user.adm_userprofile.ps16 = ps15
            user.adm_userprofile.pp17 = pp16
            user.adm_userprofile.ps17 = ps16
            user.adm_userprofile.pp18 = pp17
            user.adm_userprofile.ps18 = ps17
            user.adm_userprofile.pp19 = pp18
            user.adm_userprofile.ps19 = ps18
            user.adm_userprofile.pp20 = pp19
            user.adm_userprofile.ps20 = ps19
            user.adm_userprofile.pp21 = pp20
            user.adm_userprofile.ps21 = ps20
            user.adm_userprofile.pp22 = pp21
            user.adm_userprofile.ps22 = ps21
            user.adm_userprofile.pp23 = pp22
            user.adm_userprofile.ps23 = ps22
            ### END OF 20 NEW PASSWORDS ###

            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated')
            action = "User's password successfully updated"
            result = "Success"
            auditlog(request, "ChangePassword", action, result, request.user.username, request.user,
                     request.user.username)

            #print("Redirecting: %s" %(request.session['user_request_page']))

            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)

            try:
                return redirect(request.session['user_request_page'])
            except KeyError as ke:
                return redirect(main_app_name+':app-home-page')
            #return redirect(request.session['user_request_page'])
        else:
            action = "User unsuccessfully attempted to update password"
            result = "Fail"
            auditlog(request, "change_password", action, result, request.user.username, request.user,
                     request.user.username)
            messages.error(request, 'Please correct the error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'djams/change_password.html', {'form': form})

def passwordchanged(request):
    return render(request, 'djams/passwordchanged.html')

@login_required
def enquirylist(request):

    request_apps = request.request_apps

    if 'admin_portal' in request_apps:
        print("enquirylist: App is admin_portal. Showing all enquiries.")
        enquiry_list = ADM_UserEnquiry.objects.filter(user_id=request.user.id).exclude(status__name='Closed').order_by('-opened_date')
    
    else:
        print("enquirylist. Showing user specific enquiries")
        enquiry_list = ADM_UserEnquiry.objects.filter(user_id=request.user.id).exclude(status__name='Closed').order_by('-opened_date')

    page = request.GET.get('page', 1)

    paginator = Paginator(enquiry_list, 10)

    try:
        enquiries = paginator.page(page)
    except PageNotAnInteger:
        enquiries = paginator.page(1)
    except EmptyPage:
        enquiries = paginator.page(paginator.num_pages)
    
    return render(request, 'djams/enquiries.html', {'enquiries': enquiries})


def newenquiry(request):
    '''
    Description: Allows logged in and anonymnous users to submit an enquiry
    '''
    
    page_context = {}
    
    try:
        refnum = ADM_UserEnquiry.objects.all().aggregate(Max('id'))['id__max']
    except:
        print("newenquiry: Exception")
        refnum = 0
    try:
        refnum += 1
    except TypeError as te:
        refnum = 1

    refstring = 'AP' + str(refnum)

    print(str(request.POST))

    if request.method == 'POST' and 'send' in request.POST:
        print('newenquiry: receiving data')
        enquiryform = UserEnquiryForm(request.POST)
        print("newenquiry: Form valid: %s" %(str(enquiryform.is_valid())))
        if enquiryform.is_valid():
            enquiry_inst = enquiryform.save(commit=False)
            enquiry_inst.user = request.user
            enquiry_inst.reference = refstring
            enquiry_inst.email = request.user.email
            enquiry_inst.opened_date = datetime.datetime.today().strftime("%Y-%m-%d")
            enquiry_inst.statuschanged = datetime.datetime.today()
            enquiry_inst.creation_user = request.user
            enquiry_inst.creation_date = datetime.datetime.today().strftime('%Y-%m-%d')
            enquiry_inst.last_update_date = datetime.datetime.today().strftime('%Y-%m-%d')
            enquiry_inst.last_update_user = request.user
            enquiry_inst.save()
            action = "User created new enquiry with reference %s with ID %s"  %(str(enquiry_inst.reference), enquiry_inst.id)
            result = 'Success'
            auditlog(request, viewname="newenquiry", action=action, result=result, username=request.user.username,
             subjectuser=None, subjectusername='', client=None)
            return redirect('djams:enquiries')
    
    else:
        page_context['enquiryform'] = UserEnquiryForm()
        page_context['additional_page_context'] = {'user': request.user,
                                                    'reference': refstring,
                                                    'email': request.user.email}
    return render(request, 'djams/new_userenquiry.html', context=page_context)


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

@login_required
def status_userenquiry(request, pk):
    '''
    Description: Logged in users can view the statuses of their enquiries
    '''
    page_context = {}

    # get the record details from the database using the primary key
    userenquiry_inst = get_object_or_404(UserEnquiry, pk=pk)
    page_context['userenquiry_inst'] = userenquiry_inst
    message_list = ADM_EnquiryMessage.objects.filter(enquiry=pk).order_by('-creation_date')
    mpage_context['additional_page_context'] = {'user': request.user,
                                                'reference': 'AP' + str(userenquiry_inst.id),
                                                'email': request.user.email,
                                                }

    # Paginations
    page, paginator, messages = paginate_pages(request, page_list=message_list, page_entries=5)


    if request.method == 'POST':
        print("status_userenquiry: receiving data")
        messageform = UserEnquiryMsgForm(request.POST, prefix='msg', instance=EnquiryMessage())
        print("status_userenquiry: form is valid: %s" %(messageform.is_valid()))

        if messageform.is_valid():
            for message in message_list:
                if message.message_read == False:
                    currentmessage = ADM_EnquiryMessage.objects.get(pk=message.id)
                    currentmessage.message_read = True
                    currentmessage.save()
        message_inst = messageform.save(commit=False)
        message_inst.user = request.user
        message_inst.message_read = False
        message_inst.creation_user = request.user
        message_inst.last_update_date = datetime.datetime.today().strftime("%Y-%m-%d")
        message_inst.last_update_user = request.user
        message_inst.save()

        return redirect('djams:status-userenquiry', pk=userenquiry_inst.id)

    else:
        page_context['enquiryform'] = UserEnquiryForm(instance=userenquiry_inst)
        page_contewxt['messageform'] = UserEnquiryMsgForm(prefix='msg', instance=EnquiryMessage())

    page_context['messages'] = messages

    return render(request, 'djams/status_userenquiry.html', context=page_context)
        