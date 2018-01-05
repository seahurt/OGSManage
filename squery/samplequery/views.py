# from django.shortcuts import render,get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse, JsonResponse
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
from samplequery.models import Record,Panel,Tissues
from samplequery.serializer import RecordSerializer,TissuesSerializer,PanelSerializer,UserSerializer
from samplequery.serializerFull import RecordSerializerFull
# RecordSerializerFull add a property called <getSampleInfo> which need fetch data
# from http://medicine.1gene.com.cn/v1/api/reportInfo
import json
# from django.utils.six import BytesIO
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.contrib.auth.models import User
# from rest_framework.request import Request
# Create your views here.
#def
def getRecords(queryDict):
    result = Record.objects.all()
    if 'full_id' in queryDict and 'og_id' not in queryDict:
        # result = [x for x in result if x.full_id in queryDict['full_id']]
        result = Record.objects.filter(full_id__in=queryDict['full_id'])
    elif 'og_id' in queryDict and 'full_id' not in queryDict:
        # result = [x for x in result if x.og_id in queryDict['og_id']]
        result = Record.objects.filter(og_id__in=queryDict['og_id'])
    elif 'og_id' in queryDict and 'full_id' in queryDict:
        result = Record.objects.filter(og_id__in=queryDict['og_id'],full_id__in=queryDict['full_id'])
    else:
        result = Record.objects.all()
    if 'capm' in queryDict:
        # result = [x for x in result if x.capm in queryDict['capm']]
        result = result.filter(capm__in=queryDict['capm'])
    if 'tissue_name' in queryDict:
        # result = [ x for x in result if x.tissue_name in queryDict['tissue_name']]
        result = result.filter(tissue__tissue_name__in=queryDict['tissue_name'])
    if 'panel_name' in queryDict:
        result = result.filter(panel__panel_name__in=queryDict['panel_name'])
    if 'panel_type' in queryDict:
        # result = [ x for x in result if x.panel_type in queryDict['panel_type']]
        result = result.filter(panel__panel_type__in=queryDict['panel_type'])
    if 'panel_subtype' in queryDict:
        # result = [x for x in result if x.panel_subtype in queryDict['panel_subtype']]
        result = result.filter(panel__panel_subtype__in=queryDict['panel_subtype'])
    # print("Find:"+str(len(result)))
    return result


# API
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# API
class RecordViewSet(viewsets.ModelViewSet):
    # lookup_field = 'full_id'
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

#API
class RecordListView(generics.ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        # print(self.request.GET)
        queryDict = dict(self.request.GET)
        # print(queryDict)
        # print(queryDict.get('full_id'))
        queryset =  getRecords(queryDict)
        # print(len(queryDict['full_id']))
        return queryset
# API
@api_view(['GET'])
def FindOG(request,og_id):
    result = Record.objects.filter(og_id=og_id)
    if len(result) == 0:
        return Response(status=404)
    serializer_context = {'request': request}
    serializer = RecordSerializerFull(result,many=True,context=serializer_context)
    return Response(serializer.data,status=200)

# API
@api_view(['GET'])
def FindFullID(request,fid):
    result = Record.objects.filter(full_id=fid)
    if len(result) == 0:
        return Response(status=404)
    serializer_context = {'request': request}
    serializer = RecordSerializerFull(result,many=True,context=serializer_context)
    return Response(serializer.data,status=200)

#API
@api_view(['GET','POST'])
def query(request):
    if request.method == 'POST':
        queryDict = json.loads(request.body)
        # print(queryDict)
        result = getRecords(queryDict)
        serializer_context = {'request': request}
        # print("Query done!")
        # print(len(result))
        serializer = RecordSerializer(result,many=True,context=serializer_context)
        # serializer = RecordSerializer(result,many=True)
        return Response(serializer.data,status=200)
    elif request.method == 'GET':
        queryDict = dict(request.GET)
        # print(queryDict)
        # keys = queryDict.keys()
        # for key in keys:
        #     queryDict[key] = queryDict[key].split(',')
        result = getRecords(queryDict)
        serializer_context = {'request': request}
        serializer = RecordSerializer(result,many=True,context=serializer_context)
        # serializer = RecordSerializer(result,many=True)
        return Response(serializer.data,status=200)


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
# API
class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class PanelList(generics.ListCreateAPIView):
#     queryset = Panel.objects.all()
#     serializer_class = PanelSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class PanelDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Panel.objects.all()
#     serializer_class = PanelSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# API
class TissuesViewSet(viewsets.ModelViewSet):
    queryset = Tissues.objects.all()
    serializer_class = TissuesSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class TissuesList(generics.ListCreateAPIView):
#     queryset = Tissues.objects.all()
#     serializer_class = TissuesSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# class TissuesDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tissues.objects.all()
#     serializer_class = TissuesSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

# @api_view(['GET'])
# def api_root(request):
#     return Response({
#         'record':reverse('record-list',request=request),
#         'panel':reverse('panel-list',request=request),
#         'tissue':reverse('tissues-list',request=request)
#         })

# class RecordList(generics.ListCreateAPIView):
#     queryset = Record.objects.all()
#     serializer_class = RecordSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     # if request.method == 'GET':
#     #     records = Record.objects.all()[:20]
#     #     serializer = RecordSerializer(records,many=True)
#     #     return JsonResponse(serializer.data,safe=False)
#     # elif request.method == 'POST':
#     #     data = JSONParser().parse(request)
#     #     serializer = RecordSerializer(data=data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return JsonResponse(serializer.data,status=201)
#     #     return JsonResponse(serializer.errors,status=400)

# class RecordDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Record.objects.all()
#     serializer_class = RecordSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # record = get_object_or_404(Record,pk=pk)

    # if request.method == 'GET':
    #     serializer = RecordSerializer(record)
    #     return JsonResponse(serializer.data)

    # elif request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #     serializer = RecordSerializer(record,data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors,status=400)

    # elif request.method == 'DELETE':
    #     record.delete()
    #     return HttpResponse(status=204)

#===============================================================================


