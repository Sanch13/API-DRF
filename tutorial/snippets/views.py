from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':  # read data (many objects)
        snippets = Snippet.objects.all()  # get all objects from the DB
        serializer = SnippetSerializer(snippets, many=True)  # many=True. It means that it will
        # be many objects
        return JsonResponse(data=serializer.data, safe=False)  # return all objects format=json,
        # safe=False -> allow serializer list json

    elif request.method == 'POST':  # write data
        data = JSONParser().parse(request)  # convert byte data from stream to dict
        serializer = SnippetSerializer(data=data)  # check data out
        if serializer.is_valid():  # if data - OK? then save data to the DB
            serializer.save()  # create one object in DB
            return JsonResponse(data=serializer.data, status=201)  # return new object format=json
        return JsonResponse(serializer.errors, status=400)  # return error


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:    # try get object from pk
        snippet = Snippet.objects.get(pk=pk)  # our snippet
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)  # return error 404, page not found

    if request.method == "GET":  # read data (one object)
        serializer = SnippetSerializer(snippet)  # serializer our snippet from DB
        return JsonResponse(data=serializer.data)  # return our snippet format=json
    elif request.method == "PUT":  # update data (one object)
        data = JSONParser().parse(request)  # convert byte data from stream to dict
        serializer = SnippetSerializer(instance=snippet, data=data)  # our snippet serializer
        # with input new data. if data - OK? then save new data to the DB
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data)  # return update object format=json
        return JsonResponse(serializer.errors, status=400)  # return error

    elif request.method == "DELETE":  # delete data (one object)
        snippet.delete()  # delete our snippet
        return HttpResponse(status=204)
