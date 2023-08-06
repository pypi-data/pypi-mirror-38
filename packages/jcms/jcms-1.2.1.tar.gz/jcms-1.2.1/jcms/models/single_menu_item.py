class SingleMenuItem:
    """
    An menu item that links to a specific page
    """
    def __init__(self, title: str, slug: str):
        """

        :param title: Display title for the menu item
        :type title: str
        :param url: Django url name for the menu item
        :type url: str
        """
        self.title = title
        self.slug = slug
