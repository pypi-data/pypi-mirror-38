import importlib
'''
    Библиотечка для импорта blueprint-ов в более удобном формате
'''
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
        # Проходимся по списко в APP_LIST и импортируем данные модули
        for i in module.APP_LIST:
            try:
                file_module = importlib.import_module(i)
            except ModuleNotFoundError:
                raise ["Not module: "+i]
            app.register_blueprint(file_module.module)
