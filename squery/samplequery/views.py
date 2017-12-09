from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from samplequery.models import Record,Panel,Tissues
from samplequery.serializer import RecordSerializer
import json
from django.utils.six import BytesIO

# Create your views here.
def index(request):
    return HttpResponse("You are looking at index page!")

@csrf_exempt
def sample_list(request):
    if request.method == 'GET':
        records = Record.objects.all()[:20]
        serializer = RecordSerializer(records,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def sample_detail(request,pk):
    record = get_object_or_404(Record,pk=pk)

    if request.method == 'GET':
        serializer = RecordSerializer(record)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RecordSerializer(record,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=400)

    elif request.method == 'DELETE':
        record.delete()
        return HttpResponse(status=204)

@csrf_exempt
def sample_query(request):
    empty_post_dict = {
    'full_id':[],
    'ogid':[],
    'panel_type':[],
    'panel_subtype':[],
    'tissue_name':[],
    'capm':[]
    }
    empty_json = json.dumps(empty_post_dict)
    # print(empty_post_dict)
    # print('json',empty_json)

    if request.method == 'POST':
        post_data = json.loads(request.body)
        print(post_data)
        # print("===========================")
        # print(request.POST)
        # print(request.body)

        result = Record.objects.all() 
        if 'tissue_name' in post_data:
            result = result.filter(tissue_name__in=post_data['tissue_name'])
        if 'panel_type' in post_data:
            result = result.filter(panel_type__in=post_data['panel_type'])
        if 'panel_subtype' in post_data:
            result = result.filter(panel_subtype__in=post_data['panel_subtype'])
        if 'full_id' in post_data:
            result = result.filter(full_id__in=post_data['full_id'])
        if 'og_id' in post_data:
            result = result.filter(og_id__in=post_data['og_id'])
        if 'capm' in post_data:
            result = result.filter(capm__in=post_data['capm'])
        serializer = RecordSerializer(result,many=True)
        return JsonResponse(serializer.data,status=201,safe=False)
        # return HttpResponse('OK')
    elif request.method == 'GET':
        return JsonResponse(empty_json,safe=False)
"""
{
    'full_id':[],
    'ogid':[],
    'panel_type':[],
    'panel_subtype':[],
    'tissue_name',[],
    'capm',[],
}
"""
