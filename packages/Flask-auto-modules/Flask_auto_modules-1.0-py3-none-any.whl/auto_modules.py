from flask import current_app, _app_ctx_stack,Flask
import importlib

class AutoModules(object):

    def __init__(self,app=None,**kwargs):
        if app is not None:
            self.app = app
        else:
            raise ["Not app"]
        if 'path_list_module' in kwargs:
            self.path_list_module = kwargs['path_list_module']
        else:
            self.path_list_module = 'config.include.module_app'
        self.init_auto_module(self.app)

    def init_auto_module(self,app):
        module = importlib.import_module(self.path_list_module)
        for i in module.APP_LIST:
            try:
                file_module = importlib.import_module(i)
            except ModuleNotFoundError:
                print("Not module: "+i)
                break

            app.register_blueprint(file_module.applictaion)
