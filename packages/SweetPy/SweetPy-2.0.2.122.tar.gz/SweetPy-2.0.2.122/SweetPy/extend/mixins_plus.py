"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from __future__ import unicode_literals
import time,sys
from rest_framework import status
from rest_framework.settings import api_settings
from .response_plus import create_data,APIResponseHTTPCode,Response


class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        if hasattr(request,'tracker'):
            tracker = request.tracker
            old = time.time()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if hasattr(request, 'tracker'):
            cost_time = time.time() - old
            tracker.add_layer(func_name=self.__class__.__name__ + '.' + sys._getframe().f_code.co_name, cost_time=cost_time,
                              attributes={}, type='DataAccess')
        headers = self.get_success_headers(serializer.data)

        _data = create_data(APIResponseHTTPCode.SUCCESS, serializer.data)
        return Response(_data, status=status.HTTP_201_CREATED, headers=headers)  #Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        if hasattr(request, 'tracker'):
            tracker = request.tracker
            old = time.time()
        queryset = self.filter_queryset(self.get_queryset())
        if hasattr(request, 'tracker'):
            cost_time = time.time() - old
            tracker.add_layer(func_name=self.__class__.__name__ + '.' + sys._getframe().f_code.co_name, cost_time=cost_time,
                              attributes={}, type='DataAccess')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        _data = create_data(APIResponseHTTPCode.SUCCESS, serializer.data)
        return Response(_data)#Response(serializer.data)


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        if hasattr(request, 'tracker'):
            tracker = request.tracker
            old = time.time()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if hasattr(request, 'tracker'):
            cost_time = time.time() - old
            tracker.add_layer(func_name=self.__class__.__name__ + '.' + sys._getframe().f_code.co_name, cost_time=cost_time,
                              attributes={}, type='DataAccess')

        _data = create_data(APIResponseHTTPCode.SUCCESS, serializer.data)
        return Response(_data)  #Response(serializer.data)


class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        if hasattr(request, 'tracker'):
            tracker = request.tracker
            old = time.time()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if hasattr(request, 'tracker'):
            cost_time = time.time() - old
            tracker.add_layer(func_name=self.__class__.__name__ + '.' + sys._getframe().f_code.co_name, cost_time=cost_time,
                              attributes={}, type='DataAccess')
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        _data = create_data(APIResponseHTTPCode.SUCCESS,serializer.data)
        return Response(_data)  #Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        if hasattr(request, 'tracker'):
            tracker = request.tracker
            old = time.time()
        instance = self.get_object()
        self.perform_destroy(instance)
        if hasattr(request, 'tracker'):
            cost_time = time.time() - old
            tracker.add_layer(func_name=self.__class__.__name__ + '.' + sys._getframe().f_code.co_name, cost_time=cost_time,
                              attributes={}, type='DataAccess')

        _data = create_data(APIResponseHTTPCode.SUCCESS)
        return Response(_data)  #(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
