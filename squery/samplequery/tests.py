from django.test import TestCase,RequestFactory
from samplequery.models import Record,Panel,Tissues
from samplequery.views import getRecords,query,RecordListView
import re
import os
import json
# Create your tests here.
# full_id = models.CharField('Full ID',max_length=100,unique=True)
# og_id = models.CharField('OG ID',max_length=100)
# capm = models.CharField('CA-PM',max_length=100)
# r1 = models.CharField('R1',max_length=500)
# r2 = models.CharField('R2',max_length=500)
# tissue = models.ForeignKey(Tissues,on_delete=models.CASCADE)
# panel = models.ForeignKey(Panel,on_delete=models.CASCADE)
# create_date = models.DateTimeField(auto_now_add=True)
def setup():
        Panel.objects.create(panel_name='panel9b',panel_path="/tmp/panel9b.bed",panel_type='HC',panel_subtype='p1p4')
        Panel.objects.create(panel_name='panel3b',panel_path="/tmp/panel3b.bed",panel_type='HC',panel_subtype='p1p2')
        Panel.objects.create(panel_name='panel11b',panel_path="/tmp/panel11b.bed",panel_type='HC',panel_subtype='p1p2p4')
        Panel.objects.create(panel_name='panelM7',panel_path="/tmp/panelM7.bed",panel_type='AMP',panel_subtype='Morgene7')
        Tissues.objects.create(tissue_short_name='cfDNA',tissue_full_name='full cfDNA name')
        Tissues.objects.create(tissue_short_name='FFPE',tissue_full_name='full FFPE name')
        Tissues.objects.create(tissue_short_name='Normal',tissue_full_name='full Normal name')
        p1 = Panel.objects.get(panel_name='panel9b')
        p2 = Panel.objects.get(panel_name='panel3b')
        p3 = Panel.objects.get(panel_name='panel11b')
        p4 = Panel.objects.get(panel_name='panelM7')
        t1 = Tissues.objects.get(tissue_short_name='cfDNA')
        t2 = Tissues.objects.get(tissue_short_name='FFPE')
        t3 = Tissues.objects.get(tissue_short_name='Normal')
        fid_list = ['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b']
        tissue_map = {
            'CFD':t1,
            'FFPE':t2,
            'LEUD':t3
        }
        panel_map = {
            '9b':p1,
            '3b':p2,
            '11b':p3,
            'M7':p4
        }
        for fid in fid_list:
            og_id = re.search('OG[\d]+',fid).group(0)
            t_str = re.search('CFD|FFPE|LEUD',fid).group(0)
            capm = 'CA-PM-20171212'
            r1 = os.path.join('/tmp/',fid+'_r1.fq.gz')
            r2 = os.path.join('/tmp/',fid+'_r2.fq.gz')
            p_str = re.search('([391]+b|M[7])',fid).group(0)
            tissue = tissue_map[t_str]
            panel = panel_map[p_str]
            Record.objects.create(full_id=fid,og_id=og_id,capm=capm,r1=r1,r2=r2,tissue=tissue,panel=panel)

class getRecordsTests(TestCase):

    def setUp(self):
        setup()

    def test_queryOGID(self):
        queryDict={
            'og_id':['OG12345','OG12346','OG12347']
        }
        queryset = getRecords(queryDict)
        self.assertEqual(len(queryset),7)
        

    def test_queryFullID(self):
        queryDict = {
            'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b']
        }
        queryset = getRecords(queryDict)
        self.assertEqual(len(queryset),8)

    def test_queryBothOGID_FullID(self):
        queryDict = {
            'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b'],
            'og_id':['OG12345','OG12346','OG12347']
        }
        queryset = getRecords(queryDict)
        self.assertEqual(len(queryset),7)

    def test_queryNoOGID_FullID(self):
        queryDict = {

        }
        queryset = getRecords(queryDict)
        self.assertEqual(len(queryset),8)

class queryTests(TestCase):
    def setUp(self):
        setup()
        self.factory = RequestFactory()
    # post method test
    def test_post_query_full_id(self):
        queryDict = {'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b']}
        request = self.factory.post('/query/',data=json.dumps(queryDict),content_type='application/json')
        response = query(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),8)

    def test_post_query_og_id(self):
        queryDict={
            'og_id':['OG12345','OG12346','OG12347']
        }
        request = self.factory.post('/query/',data=json.dumps(queryDict),content_type='application/json')
        response = query(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),7)

    def test_post_query_Both_OG_Full_id(self):

        queryDict = {
            'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b'],
            'og_id':['OG12345','OG12346','OG12347']
        }
        request = self.factory.post('/query/',data=json.dumps(queryDict),content_type='application/json')
        # print(request.POST)
        response = query(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),7)

    def test_post_query_no_OG_Full_id(self):
        queryDict = {}  
        request = self.factory.post('/query/',data=json.dumps(queryDict),content_type='application/json')
        response = query(request)
        self.assertEqual(response.status_code,200)
        # print(response.data)
        self.assertEqual(len(response.data),8)


    # get method test
    def test_get_query_full_id(self):
        queryDict = {'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b']}
        request = self.factory.get('/query/',queryDict)
        response = query(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data),8)
    def test_get_query_og_id(self):
        queryDict={
            'og_id':['OG12345','OG12346','OG12347']
        }
        request = self.factory.get('/query/',queryDict)
        response = query(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),7)
    def test_get_query_Both_OG_Full_id(self):
        queryDict = {
            'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b'],
            'og_id':['OG12345','OG12346','OG12347']
        }
        request = self.factory.get('/query/',queryDict)
        response = query(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),7)
    def test_get_query_no_OG_Full_id(self):
        queryDict = {}  
        request = self.factory.get('/query/',queryDict)
        # print(request.__dict__)
        response = query(request)
        self.assertEqual(response.status_code,200)
        # print(response.data)
        self.assertEqual(len(response.data),8)

class RecordListViewTests(TestCase):
    def setUp(self):
        setup()
        self.factory = RequestFactory()

    def test_get_query_full_id(self):
        queryDict = {'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b']}
        request = self.factory.get('/list/',queryDict)
        response = RecordListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('results')),8)
    def test_get_query_og_id(self):
        queryDict={
            'og_id':['OG12345','OG12346','OG12347']
        }
        request = self.factory.get('/list/',queryDict)
        response = RecordListView.as_view()(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data.get('results')),7)
    def test_get_query_Both_OG_Full_id(self):
        queryDict = {
            'full_id':['OG12345CFD3b','OG12346CFD9b','OG12347CFD11b','OG12345FFPE3b','OG12345LEUD3b',
                    'OG12346FFPE3b','OG12347FFPEM7','OG12348LEUD9b'],
            'og_id':['OG12345','OG12346','OG12347']
        }
        request = self.factory.get('/list/',queryDict)
        response = RecordListView.as_view()(request)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data.get('results')),7)
    def test_get_query_no_OG_Full_id(self):
        queryDict = {}  
        request = self.factory.get('/list/',queryDict)
        # print(request.__dict__)
        response = RecordListView.as_view()(request)
        self.assertEqual(response.status_code,200)
        # print(response.data)
        # print(response.__dict__)
        self.assertEqual(len(response.data.get('results')),8)
