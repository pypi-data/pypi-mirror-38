''' 
These are the middleware bindings for routing authentication, access to master data and client specific database queries 
'''

import threading
from django.conf import settings

MASTER_DATASTORE = 'MDS'
MASTER_ADMIN_DATASTORE = 'MDS'
MASTER_ADMIN_APP_LABELS = ['auth', 'accounts', 'sessions', 'view_authorities', 'view_user_clients', 'djams', 'admin_portal', 'app_portal']
MASTER_ADMIN_MODEL_LABELS = ['statelessapp', ]
SUB_CLIENT_MODEL_FLAGS = ['rds_', 'tds_', 'ads_']
SUB_CLIENT_DB_FLAGS = ['RDS_', 'TDS_', 'ADS_']

# object to hold request data
request_cfg = threading.local()

class BaseMiddleware:
    '''
    Description: The base middleware, which determines the main microsite application being used, determined by the AUTHORIZED_APPS variable in the settings.py file of the main app
                 that is requesting access. The name of this app is then used for authenticaiton and audit purposes by the djams app.
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        request.request_apps = settings.DJAMS_AUTHORIZED_APPS
        request.use_microsite_auth = settings.DJAMS_MICROSITE_AUTHENTICATION
        response = self.get_response(request)
        return response

class DBRouterMiddleware(object):
    '''
    Description: This middlwares functions include:
                1. Sets a flag if we are acccessing Django admin in order to prevent database rerouting for the auth model. It then removes the flag once the request is processed
                2. Sets and uses the relevant client specific databases on a threaded request object
    '''

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, args, kwargs):
        
        if request.path.startswith('/admin'):
            request_cfg.admin = True
        

        try: # else raise error if not logged in
            if request.session['rds']:
                request_cfg.cfg_rds = request.session['rds']
                request_cfg.cfg_tds = request.session['tds']
                request_cfg.cfg_ads = request.sessions['ads']

        except KeyError as ke:
            pass
        except AttributeError as ke:
            pass


    def process_response(self, request, response):

        if hasattr(request_cfg, 'admin'):
            del request_cfg.admin

        if request_cfg['rds']:
            request_cfg.cfg_rds = request.session['rds']
            request_cfg.cfg_tds = request.session['tds']
            request_cfg.cfg_ads = request.session['ads']

    def process_request(self, request, response):
        
        if request_cfg['rds']:
            request_cfg.cfg_rds = request.session['rds']
            request_cfg.cfg_tds = request.session['tds']
            request_cfg.cfg_ads = request.session['ads']

class UserSessionRouter(object):

    '''
    Description: Redirects database IO for the Django auth and sessions. This maintains authentication between microsite apps
    '''

    def db_for_read(self, model, **hints):

        if not hasattr(request_cfg, 'admin'):

            if model._meta.app_label in MASTER_ADMIN_APP_LABELS:
                return MASTER_ADMIN_DATASTORE

            elif model.__name__.lower() in MASTER_ADMIN_MODEL_LABELS:
                return MASTER_ADMIN_DATASTORE

        
        return None

    def db_for_write(self, model, **hints):

        if not hasattr(request_cfg, 'admin'):
            if model._meta.app_label in MASTER_ADMIN_APP_LABELS:
                return MASTER_ADMIN_DATASTORE

            elif model.__name__.lower() in MASTER_ADMIN_MODEL_LABELS:
                return MASTER_ADMIN_DATASTORE

        return None

    def allow_relation(self, obj1, obj2, **hints):

        '''
        Description: Determines whether relationship is allowed between two objects
        '''
        # allow any relation:
        
        return True

class SubClientDBRouter:
    '''
    Description: Each client should have at least 3 databases: Raw datastore (RDS), Transactional datastore (TDS) and Analytical datastore (ADS). An apps data models should reflect this
                and the router uses this information to direct the queries to the relevant datastore.
    '''

    def db_for_read(self, model, **hints):

        try:
            if 'rds_' in model.__name__.lower():
                return str(request_cfg.cfg_rds)

            elif 'tds_' in model.__name__.lower():
                return str(request_cfg.cfg_tds)

            elif 'ads_' in model.__name__.lower():
                return str(request_cfg.cfg_ads)
        
        except AttributeError as AE:
            return None
        
        return None

    def db_for_write(self, model, **hints):

        try:
            if 'rds_' in model.__name__.lower() and hasattr(request_cfg, 'cfg_rds'):
                return str(request_cfg.cfg_rds)

            elif 'tds_' in model.__name__.lower() and hasattr(request_cfg, 'cfg_tds'):
                return str(request_cfg.cfg_tds)

            elif 'ads_' in model.__name__.lower() and hasattr(request_cfg, 'cfg_ads'):
                return str(request_cfg.cfg_ads)
        
        except AttributeError as AE:
            return None
        
        return None
    
    def allow_migrate(self, db, app_label=None, model_name=None, **hints):

        '''
        Description: Make sure the auth app does not appear in the RDS, TDS or ADS database
        '''

        # if the database nisn't client specific i.e. doesnt have 'RDS_', 'TDS_', 'ADS_' in the name, allow migrations to their natural database
        if db[0:4] not in SUB_CLIENT_DB_FLAGS:
            return True

        if "RDS_" in db:
            if model_name != None:
                if 'rds_' in model_name.lower():
                    return True

        elif "TDS_" in db:
            if 'tds_' in model_name.lower():
                return True

        elif "ADS_" in db:
            if 'ads_' in model_name.lower():
                return True

        if app_label == 'django_plotly_dash':
            return True
        
        
        return False
        


    # def allow_relation(self, obj1, obj2, **hints):

    #     '''
    #     Description: Determines whether relationship is allowed between two objects
    #     '''
    #     # allow any relation:
        
    #     return True
