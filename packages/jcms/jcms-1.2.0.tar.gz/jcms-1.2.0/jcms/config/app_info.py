import importlib
from jcms.config.jcms_settings import JcmsSettings
from jcms.components.util import warn

APPS_SUBMODULE = 'APPS'


class AppInfo(object):
    """
    Singleton that handles the info per app
    """

    _instance = None

    class __AppInfo:
        """
        Private class for the singleton
        """

        JCMS_APPS = {}

        def __init__(self):
            """
            Initiate the jcms apps by getting the jcms.py for each jcms app
            """

            apps = JcmsSettings.get_setting(APPS_SUBMODULE)
            apps.append('jcms')

            for jcms_app in apps:
                try:
                    self.JCMS_APPS[jcms_app] = importlib.import_module(jcms_app + '.jcms')
                except ModuleNotFoundError:
                    warn('JCMS app {0} does not have a jcms.py. Please create a the jcms.py in the {0} '
                                         'app or delete it from JCMS.APPS'.format(jcms_app.upper()))

    def __new__(self):
        """
        Override the new method so there can only be one instance of this object
        """

        if not self._instance:
            self._instance = self.__AppInfo()

        return self._instance

    def __getattr__(self, name):
        """
        Override getattr method so the getattr function will be ran on the private class
        """

        return getattr(self._instance, name)
