from jcms.components.util import app_has_attr
from jcms.config import AppInfo
from jcms.generators.url_generator import UrlGenerator


class UrlParser:
    """
    This class parses all the generators to actual paths that can be used by django
    """

    @staticmethod
    def get_urls():
        """
        Gets the generators for each app and converts them to paths

        :return List of paths added via jcms
        :rtype list
        """

        urls = []
        app_info = AppInfo()

        for app_name, app_data in app_info.JCMS_APPS.items():
            if app_has_attr(app_name, app_data, 'urlpatterns', list):
                for urlpattern in app_data.urlpatterns:
                    if isinstance(urlpattern, UrlGenerator):
                        urls += urlpattern.get_urls()

        return urls
