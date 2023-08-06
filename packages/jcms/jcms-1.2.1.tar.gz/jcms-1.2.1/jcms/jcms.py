from django.contrib.auth.models import User, Group

from jcms.components import NoConfig
from jcms.models import Option, Article
from jcms.generators import CMSGenerator

option_view = CMSGenerator(Option, ['type', 'value'])
articles_view = CMSGenerator(Article, ['code', 'title', 'content'], ['code', 'title'])
user_view = CMSGenerator(User, ['username', 'first_name', 'last_name', 'email', 'password', 'groups', 'is_staff',
                              'is_active', 'is_superuser'], ['username', 'email', 'groups', 'is_active'])
groups_view = CMSGenerator(Group, ['name', 'permissions'])

urlpatterns = [
    option_view,
    articles_view,
    user_view,
    groups_view
]

menu_item = NoConfig
