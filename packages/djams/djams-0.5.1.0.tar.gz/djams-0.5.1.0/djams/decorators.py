from django.core.exceptions import PermissionDenied
from .models import ADM_Authority, ADM_App
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse


def login_app_required(function, redirect_field_name=None, login_url='login/'):
    
    '''
    Description: Checks users are logged in and subscribed to the current app
    '''

    def wrap(request, *args, **kwargs):

        # check auth:
        if not request.user.is_authenticated:
            request.session['user_request_page'] = request.path
            return redirect(login_url)
        
        app_name = request.resolver_match.app_name

        print("app_name: %s" %(app_name))

        # get the microsite / app name and check in the session whether they have already been authorized:
        # main_app_name = settings.DJAMS_AUTHORIZED_APPS[0].split('.')[0]
        user_auth_dict = request.session.get('user_app_auths', {})
        user_app_auth = user_auth_dict.get(app_name, False)
        print("Previous user app auth: %s" % (str(user_app_auth)))

        if user_app_auth:  # if previously authorized in the session, return the view
            print("login_app_required: :User previously permitted in session to use app.")
            return function(request, *args, **kwargs)
        
        else: # else perform checks that involve transactions to the database: 
            current_app = ADM_App.objects.get(django_app_name=app_name)
            app_authority = ADM_Authority.objects.filter(user=request.user, app=current_app).first()
            # print("user: %s" %(request.user.id))
            # print("current_app: %s" %(current_app.id))
            # print("Authority: %s" %(str(app_authority)))

            if app_authority:
                print("login_app_required: setting user_app_auth for current app as authenticated.")
                user_auth_dict[app_name] = True
                request.session['user_app_auths'] = user_auth_dict
                return function(request, *args, **kwargs)
            else:
                message = 'You need to be subscribed to an app in order to gain access to this page. Please contact the adminstrator / owner of the app you wish to view.'
                return HttpResponse(message, status=401)


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def login_app_client_required(function, redirect_field_name=None, login_url=None):
    '''
    Description: Checks users are logged in and subscribed to the current app
    '''

    def wrap(request, *args, **kwargs):

        # check auth:
        if not request.user.is_authenticated:
            return redirect(login_url)

        # get the microsite / app name and check in the session whether they have already been authorized:
        app_name = request.resolver_match.app_name
        client = request.session.get('myclient', False)

        user_app_auth = request.session.get('user_app_client_auth', {}).get(app_name, False)
        # print("user_app_auth: %s" % (str(user_app_auth)))

        if user_app_auth:  # if previously authorized in the session, return the view
            print("login_app_client_required: :User previously permitted in session to use app and client combination.")
            return function(request, *args, **kwargs)

        else:  # else perform checks that involve db transactions:
            current_app = App.objects.get(django_app_name=app_name)
            app_authority = Authority.objects.filter(
                user=request.user, app=current_app).first()
            
            # print("user: %s" % (request.user.id))
            # print("current_app: %s" % (current_app.id))
            # print("Authority: %s" % (str(authority)))

            if app_authority and client:
                print("login_app_required: setting user_app_auth for current app as authenticated.")
                request.session.get('user_app_auth', {})[app_name] = True
                return function(request, *args, **kwargs)

            elif app_authority and not client:
                return redirect('etca_bindings:my-clients')

            else:
                raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
