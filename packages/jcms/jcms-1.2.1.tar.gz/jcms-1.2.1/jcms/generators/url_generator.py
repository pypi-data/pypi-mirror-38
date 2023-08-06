from abc import ABCMeta, abstractmethod


class UrlGenerator:
    """
    Interface that need to be implemented for urlpatterns in jcms.py
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_urls(self):
        pass
