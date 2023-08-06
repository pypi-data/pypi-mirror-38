from django.conf import settings
from jcms.exceptions import JcmsVariableMissingException, SubmoduleMissingException


class JcmsSettings(object):
    """
    Manage jcms settings from django settings
    """

    @staticmethod
    def get_setting(submodule: str =''):
        """
        Gets a setting for jcms

        :param submodule: A submodule of the jcms setting
        :type submodule: str

        :raises JcmsVariableMissing: JCMS cannot be found in the django settings
        :raises SubmoduleMissing: Submodule that is requested is not in the JCMS variable in the django settings
        """

        if hasattr(settings, 'JCMS'):
            if submodule in settings.JCMS:
                return settings.JCMS[submodule]
            else:
                raise SubmoduleMissingException('No APPS list in the JCMS settings')
        else:
            raise JcmsVariableMissingException('No JCMS dict in settings')
