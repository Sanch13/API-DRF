from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, \
    HTTP_201_CREATED
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


###################################################################################################
# create api with regular Django views
# @csrf_exempt
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':  # read data (many objects)
#         snippets = Snippet.objects.all()  # get all objects from the DB
#         serializer = SnippetSerializer(snippets, many=True)  # many=True. It means that it will
#         # be many objects
#         return JsonResponse(data=serializer.data, safe=False)  # return all objects format=json,
#         # safe=False -> allow serializer list json
#
#     elif request.method == 'POST':  # write data
#         data = JSONParser().parse(request)  # convert byte data from stream to dict
#         serializer = SnippetSerializer(data=data)  # check data out
#         if serializer.is_valid():  # if data - OK? then save data to the DB
#             serializer.save()  # create new object in DB
#             return JsonResponse(data=serializer.data, status=HTTP_201_CREATED)  # return new object
#             # format=json
#         return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)  # return error
#
#
# @csrf_exempt
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:    # try get object from DB on pk
#         snippet = Snippet.objects.get(pk=pk)  # our snippet
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=HTTP_404_NOT_FOUND)  # return error 404, page not found
#
#     if request.method == "GET":  # read data (one object)
#         serializer = SnippetSerializer(snippet)  # serializer our snippet from DB
#         return JsonResponse(data=serializer.data)  # return our snippet format=json
#     elif request.method == "PUT":  # update data (one object)
#         data = JSONParser().parse(request)  # convert byte data from stream to dict
#         serializer = SnippetSerializer(instance=snippet, data=data)  # our snippet serializer
#         # with input new data. if data - OK? then save new data to the DB
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(data=serializer.data)  # return update object format=json
#         return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)  # return error
#
#     elif request.method == "DELETE":  # delete data (one object)
#         snippet.delete()  # delete our snippet
#         return HttpResponse(status=HTTP_204_NO_CONTENT)
###################################################################################################
# create api with DRF and decoration @api_view
# add optional format suffixes -> format=None
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):  # def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':  # read data (many objects)
#         snippets = Snippet.objects.all()  # get all objects from the DB
#         serializer = SnippetSerializer(snippets, many=True)  # many=True. It means that it will
#         # be many objects
#         return Response(data=serializer.data)  # return all objects format=json,
#
#     elif request.method == 'POST':  # write data
#         serializer = SnippetSerializer(data=request.data)  # check data out
#         if serializer.is_valid():  # if data - OK? then save data to the DB
#             serializer.save()  # create new object in DB
#             return Response(data=serializer.data, status=HTTP_201_CREATED)  # return new object
#             # format=json
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)  # return error
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):  # def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:    # try get object from DB on pk
#         snippet = Snippet.objects.get(pk=pk)  # our snippet
#     except Snippet.DoesNotExist:
#         return Response(status=HTTP_404_NOT_FOUND)  # return error 404, page not found
#
#     if request.method == "GET":  # read data (one object)
#         serializer = SnippetSerializer(snippet)  # serializer our snippet from DB
#         return Response(data=serializer.data)  # return our snippet format=json-object
#
#     elif request.method == "PUT":  # update data (one object)
#         serializer = SnippetSerializer(instance=snippet, data=request.data)  # our snippet
#         # serializer with input new data. if data - OK? then save new data to the DB
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data)  # return update object format=json-object
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)  # return error
#
#     elif request.method == "DELETE":  # delete data (one object)
#         snippet.delete()  # delete our snippet
#         return Response(status=HTTP_204_NO_CONTENT)
###################################################################################################
# rewriting the root view as a class-based view
#
# class SnippetList(APIView):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()  # get all objects from the DB
#         serializer = SnippetSerializer(snippets, many=True)  # many=True. It means that it will
#         return Response(data=serializer.data)  # return all objects format=json,
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)  # check data out
#         if serializer.is_valid():  # if data - OK? then save data to the DB
#             serializer.save()  # create new object in DB
#             return Response(data=serializer.data, status=HTTP_201_CREATED)  # return new object
#             # format=json
#         return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)  # return error
#
#
# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     def get_object(self, pk):
#         try:  # try get object from DB on pk
#             return Snippet.objects.get(pk=pk)  # our snippet
#         except Snippet.DoesNotExist:
#             return Http404  # return error 404, page not found
#
#     def get(self, request, pk, format=None): # get object from DB on pk
#         snippet = self.get_object(pk=pk)
#         serializer = SnippetSerializer(snippet)  # serializer our snippet from DB
#         return Response(data=serializer.data)  # return our snippet format=json-object
#
#     def put(self, request, pk, format=None):  # update data (one object)
#         snippet = self.get_object(pk=pk) # get object from DB on pk
#         serializer = SnippetSerializer(instance=snippet, data=request.data)  # serializer our snippet
#         # from DB with an input new data
#         if serializer.is_valid():  # if data - OK? then save new data to the DB
#             serializer.save()
#             return Response(data=serializer.data)  # return update object format=json-object
#         return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)  # return error
#
#     def delete(self, request, pk, format=None):  # delete data (one object) from the DB
#         snippet = self.get_object(pk=pk)  # get object from DB on pk
#         snippet.delete()  # delete our snippet
#         return Response(status=HTTP_204_NO_CONTENT)
###################################################################################################
# rewrite the views by using the mixin classes.

# class SnippetList(mixins.ListModelMixin,  # provides to get all the objects
#                   mixins.CreateModelMixin,  # provides to create a new object
#                   generics.GenericAPIView):  # basic class provides all the functions for django
#
#     queryset = Snippet.objects.all()  # defines the objects that will be access through the view
#     serializer_class = SnippetSerializer  # specifies which serializer will be used to convert
#     # in JSON format and back
#
#     def get(self, request, *args, **kwargs):  # method list() provides getting all the objects
#         return self.list(request=request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):  # method create() provides creating a new object
#         return self.create(request=request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,  # provides to get one object
#                     mixins.UpdateModelMixin,  # provides to update one object
#                     mixins.DestroyModelMixin,  # provides to delete one object
#                     generics.GenericAPIView):  # basic class provides all the functions for django
#
#     queryset = Snippet.objects.all()  # defines the objects that will be access through the view
#     serializer_class = SnippetSerializer  # specifies which serializer will be used to convert
#     # in JSON format and back
#
#     def get(self, request, *args, **kwargs):  # method retrieve() provides getting one object
#         return self.retrieve(request=request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):  # method update() provides updating one object
#         return self.update(request=request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):  # method destroy() provides deleting one object
#         return self.destroy(request=request, *args, **kwargs)
###################################################################################################
# Using generic class-based views
class SnippetList(generics.ListCreateAPIView):  # provides using GET, POST

    queryset = Snippet.objects.all()  # defines the objects that will be access through the view
    serializer_class = SnippetSerializer  # specifies which serializer will be used to convert
    # in JSON format and back


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):  # provides using GET, PUT, DELETE

    queryset = Snippet.objects.all()  # defines the objects that will be access through the view
    serializer_class = SnippetSerializer  # specifies which serializer will be used to convert
    # in JSON format and back
