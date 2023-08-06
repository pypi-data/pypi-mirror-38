from typing import List
from django.template.defaultfilters import slugify
from jcms.models.single_menu_item import SingleMenuItem


class GenericMenuItem:
    """
    Generic menu item that can be seen in the left bar in the cms
    """

    def __init__(self, title: str, single_menu_items: List[SingleMenuItem], slug: str = False):
        """
        :param slug: The slug the single menu items will have in front of them
        :type slug: str
        :param title: Display name for the MenuItem
        :type title: str
        :param single_menu_items: SingleMenuItems that are shown as children
        :type single_menu_items: List[SingleMenuItem]
        """

        if slug:
            self.slug = slug
        else:
            self.slug = slugify(title)

        self.title = title
        self.single_menu_items = single_menu_items
