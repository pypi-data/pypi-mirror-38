from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import path
from abc import ABCMeta
from .url_generator import UrlGenerator


class CMSGenerator(UrlGenerator):
    """
    Creates a cms crud for the model
    """

    __metaclass__ = ABCMeta

    def __init__(self, model, create_edit_list, list_fields=[], icon=''):
        self.model = model
        self.create_edit_list = create_edit_list
        self.list_fields = list_fields and list_fields or create_edit_list
        self.icon = icon
        self.model_name = model.__name__.lower()

    def get_urls(self):
        """
        Gets all url objects for to create the urls

        :return: List[path]
        """

        return [
            path(self.model_name + '/', self.list_view(), name=self.model_name + 'List'),
            path(self.model_name + '/create/', self.create_view(), name=self.model_name + 'Create'),
            path(self.model_name + '/<pk>/', self.detail_view(), name=self.model_name + 'Detail'),
            path(self.model_name + '/<pk>/edit/', self.edit_view(), name=self.model_name + 'Edit'),
            path(self.model_name + '/<pk>/delete/', self.delete_view(), name=self.model_name + 'Delete'),
        ]

    def base_view_class(self):
        """
        Creates a class that has the basic features for each view

        :return: BaseViewClass
        """
        class BaseViewClass(LoginRequiredMixin, PermissionRequiredMixin):
            model = self.model
            permission_required = 'jcms.create_' + self.model_name

        return BaseViewClass

    def create_edit_class(self):
        """
        Creates a class for the create and edit view

        :return: CreateEditClass
        """

        class CreateEditClass(self.base_view_class()):
            fields = self.create_edit_list
            template_name = 'jcms-admin/crud/edit_or_create.html'
            success_url = reverse_lazy('jcms:' + self.model_name + 'List')

        return CreateEditClass

    def list_view(self):
        """
        This creates the view for the list. With permission create_<model_name>

        :return: ObjectList
        """
        main = self

        class ObjectList(self.base_view_class(), ListView):
            fields = self.list_fields
            template_name = 'jcms-admin/crud/list.html'

            def get_queryset(self):
                query_set = main.get_search_queryset(self)
                if query_set:
                    return query_set

                return super(ObjectList, self).get_queryset()

        return ObjectList.as_view()

    def detail_view(self):
        """
        @todo implement
        Detail view. With permission create_<model_name>

        :return: ObjectDetail
        """

        class ObjectDetail(self.base_view_class(), DetailView):
            template_name = 'jcms-admin/crud/detail.html'

        return ObjectDetail.as_view()

    def create_view(self):
        """
        Creates the view for the creation of the model

        :return: ObjectCreate
        """

        class ObjectCreate(self.create_edit_class(), SuccessMessageMixin, CreateView):
            success_message = 'Successfully created ' + self.model_name

        return ObjectCreate.as_view()

    def edit_view(self):
        """
        Creates the view for editing. With permission change_<model_name>

        :return: ObjectEdit
        """

        class ObjectEdit(self.create_edit_class(), SuccessMessageMixin, UpdateView):
            permission_required = 'jcms.change_' + self.model_name
            success_message = 'Successfully edited ' + self.model_name

        return ObjectEdit.as_view()

    def delete_view(self):
        """
        Creates the delete view. With permission delete_<model_name>

        :return: ObjectDelete
        """

        class ObjectDelete(self.base_view_class(), DeleteView):
            permission_required = 'jcms.delete_' + self.model_name
            success_url = reverse_lazy('jcms:' + self.model_name + 'List')
            success_message = 'Successfully deleted ' + self.model_name

            def delete(self, request, *args, **kwargs):
                messages.success(self.request, self.success_message)
                return super(ObjectDelete, self).delete(request, *args, **kwargs)

        return ObjectDelete.as_view()

    @staticmethod
    def get_search_queryset(generic_list):
        """
        Gets the search query for the object

        :return: Queryset
        """

        search_term = generic_list.request.GET.get('search')
        if search_term:
            queries = [Q(**{f + '__icontains': search_term}) for f in generic_list.fields]
            qs = Q()
            for query in queries:
                qs = qs | query

            return generic_list.model.objects.filter(qs)

        return None
