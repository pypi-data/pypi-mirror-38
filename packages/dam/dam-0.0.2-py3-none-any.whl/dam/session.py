from .authsession import AuthSession
from .app import App


class Session(AuthSession):
    def __init__(self, token):
        super().__init__(token)

    def get_apps(self):
        """ Get a list of your dev apps.

            :rtype:
                list of apps
            :returns:
                A list of app sessions
        """

        app_link = 'https://discordapp.com/api/oauth2/applications'
        apps_json = self.get(app_link).json()

        get_app = lambda app: App(app['id'], app['name'], self.token)
        return [get_app(app) for app in apps_json]

    def get_app(self, id=None, name=None):
        """ Get an app by its name or ID.

            :param str id:
                App's Client ID
            :param str name:
                App name
            :rtype:
                App
            :returns:
                An app session
        """

        if not id and not name:
            raise ValueError('No input given.')

        for app in self.get_apps():
            if app.id == id:
                return app
            elif app.name == name:
                return app
