Библиотечка для импорта blueprint-ов в более удобном формате

    #apps.user.app
        from flask import Blueprint
        applictaion = Blueprint('user', __name__, url_prefix='/')
    
    # settings.app
        LIST_APP = ['apps.user.app']
    
    # app.py
        from auto_modules.auto_modules import AutoModules
        # path_list_module - Путь к файлу где находится ваш LIST_APP
        AutoModules(app,path_list_module='settings.app')
    
И все, все ваши blueprint-ы будут подключены, в планах расширить функционал
пока это лишь небольшой набросок, хочу сделать флягу более полной в плане модульности.
Возможно данная библиотечка пойдет основой для каркаса связки множество моих наработок.

    Так-же есть возможность создать модули через команду create ./PATH/module_name
    и скрипт создать скелет с blueprint-ом.

Поддержка от Python 3.6 и выше.