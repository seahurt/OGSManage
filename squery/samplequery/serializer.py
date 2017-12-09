#!python
from django.forms import widgets
from rest_framework import serializers
from samplequery.models import Record,Tissues,Panel


class RecordSerializer(serializers.ModelSerializer):
    # tissue = serializers.ReadOnlyField(source='Tissues.tissue_short_name')
    # panel = serializers.ReadOnlyField(source="Panel.panr.el_name")
    class Meta():
        model = Record
        # fields = ('id','full_id','og_id','capm','r1','r2','tissue','panel','tissue_name','panel_path','panel_type')
        fields = ('id','full_id','og_id','capm','r1','r2','tissue','panel','panel_path','panel_type')
    
    # def create(self,validated_data):
    #     return Record.objects.create(**validated_data)

    # def update(self,instance,validated_data):
    #     instance.full_id = validated_data.get('full_id', instance.full_id)
    #     instance.og_id = validated_data.get('og_id', instance.og_id)
    #     instance.capm = validated_data.get('capm', instance.capm)
    #     instance.r1 = validated_data.get('r1', instance.r1)
    #     instance.r2 = validated_data.get('r2', instance.r2)
    #     instance.tissue = validated_data.get('tissue', instance.tissue)
    #     instance.panel = validated_data.get('panel',instance.panel)
    #     instance.tissue = Tissues.objects.get(pk=instance.tissue)
    #     instance.panel = Panel.objects.get(pk=instance.panel)
    #     instance.save()
    #     return instance
    # def is_valid(self,data):
    #     full_id = data.get('full_id')
    #     og_id = data.get('og_id')
    #     capm = data.get('r1')



