from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets, serializers
from rest_framework import routers
from .url_generator import UrlGenerator


class APIGenerator(UrlGenerator):
    """
    Generates an api based on a model
    """

    def __init__( self, model, basis_fields, lookup_field='pk', methods=[], method_fields={}, all=False):
        self.model = model
        self.basis_fields = basis_fields
        self.lookup_field = lookup_field

        self.methods = methods
        self.method_fields = method_fields

        self.all = all

        # Variables that are used very often
        self.model_name = model.__name__.lower()

    def get_urls(self):
        """
        Creates the urls

        :return: List[url]
        """
        view = self.get_model_set()
        router = routers.SimpleRouter()
        router.register('api/' + self.model_name, view)

        return router.urls

    def get_model_set(self):
        """
        Creates model view set for a model

        :return: ModelViewSet
        """

        main = self

        class ObjectModelSet(viewsets.ModelViewSet):
            queryset = main.model.objects.all()
            lookup_field = main.lookup_field
            filter_fields = 'overview' in main.method_fields and main.method_fields['overview'] or main.basis_fields

            def list(self, request, *args, **kwargs):
                if 'overview' in main.method_fields or main.all:
                    return super(ObjectModelSet, self).list(request, args, kwargs)
                raise MethodNotAllowed('Overview or all is not turned on')

            def create(self, request, *args, **kwargs):
                if 'create' in main.method_fields or main.all:
                    return super(ObjectModelSet, self).create(request, *args, **kwargs)
                raise MethodNotAllowed('Create or all is not turned on')

            def retrieve(self, request, *args, **kwargs):
                if 'retrieve' in main.method_fields or main.all:
                    return super(ObjectModelSet, self).retrieve(request, *args, **kwargs)
                raise MethodNotAllowed('Retrieve or all is not turned on')

            def update(self, request, *args, **kwargs):
                if 'update' in main.method_fields or main.all:
                    return super(ObjectModelSet, self).update(request, *args, **kwargs)
                raise MethodNotAllowed('Update or all is not turned on')

            def partial_update(self, request, *args, **kwargs):
                if 'update' in main.method_fields or main.all:
                    return super(ObjectModelSet, self).partial_update(request, *args, **kwargs)
                raise MethodNotAllowed('Update or all is not turned on')

            def destroy(self, request, *args, **kwargs):
                if 'destroy' in main.method_fields or main.all:
                    return super(ObjectModelSet, self).destroy(request, *args, **kwargs)
                raise MethodNotAllowed('Destroy or all is not turned on')

            def get_serializer_class(self):
                if self.action in main.method_fields:
                    return main.create_serializer(main.model, main.method_fields[self.action])

                return main.create_serializer(main.model, main.basis_fields)

        return ObjectModelSet

    @staticmethod
    def create_serializer(api_model, serialize_fields):
        """
        Creates a serializer of the model

        :param api_model:
        :param serialize_fields:
        :return: ModelSerializer
        """

        class ModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = api_model
                fields = serialize_fields

        return ModelSerializer
