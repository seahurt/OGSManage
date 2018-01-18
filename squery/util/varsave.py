#!python3
import setup
setup.init()
from varystore.models import Tumor, Gene, Site, Drug, Package, Patient, Sample, Snv, Cnv, DrugRecord
from samplequery.models import Record
from repbin import get_md5_url
import pandas as pd
# import json
# from multiprocessing import Process
from django.core.exceptions import ObjectDoesNotExist
import re


class SampSave():
    anno_colnames = ["Chr", "Start", "End", "Ref", "Alt", "Func.refGene",
                     "Gene.refGene", "GeneDetail.refGene", "ExonicFunc.refGene",
                     "AAChange.refGene", "cosmic83", "CLINSIG", "CLNDBN", "CLNACC",
                     "CLNDSDB", "CLNDSDBID", "SIFT_score", "SIFT_pred",
                     "Polyphen2_HDIV_score", "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score",
                     "Polyphen2_HVAR_pred", "LRT_score", "LRT_pred", "MutationTaster_score",
                     "MutationTaster_pred", "MutationAssessor_score", "MutationAssessor_pred",
                     "FATHMM_score", "FATHMM_pred", "RadialSVM_score", "RadialSVM_pred",
                     "LR_score", "LR_pred", "VEST3_score", "CADD_raw", "CADD_phred",
                     "GERP++_RS", "phyloP46way_placental", "phyloP100way_vertebrate",
                     "SiPhy_29way_logOdds", "avsnp150", "1000g2015aug_all",
                     "Otherinfo", "sp1", "sp2", "sp3", "sp4", "sp5", "sp6", "sp7", "sp8",
                     "sp9", 'varinfo']

    def __init__(self, report_fmt, annovar_raw, full_id, cnv_fmt):
        self.report_fmt = report_fmt
        self.annovar_raw = annovar_raw
        self.cnv_fmt = cnv_fmt
        self.full_id = full_id
        self.record = Record.objects.get(full_id=self.full_id)
        self.tissue = self.record.tissue
        self.og_id = self.record.og_id
        self.patient = self.get_patientinfo()
        self.sample = self.get_sample()
        self.get_snv()
        self.get_cnv()

    def get_patientinfo(self):
        try:
            p = self.record.sample.all()[0].patient
        except ObjectDoesNotExist:
            jsondata = get_md5_url.SampleInfo(self.og_id).data
            # data = json.loads(patient_json)
            if jsondata['success'] is True:
                self.data = jsondata['data']
                p = Patient()
                p.name = self.data['name']
                p.gender = 'M' if self.data['gender'] == '男' else 'F'
                p.age = int(self.data['age'])
                p.id_number = self.data['ID_number']
                p.tumor_type = self.get_tumor()
                p.hospital = self.data['hospital']
                p.service_package = self.get_package()
                p.full_clean()
                p.save()
                return p
            else:
                return None
        return p

    def get_tumor(self):
        try:
            t = Tumor.objects.get(name=self.data['tumour_name'])
        except ObjectDoesNotExist:
            t = Tumor()
            t.name = self.data['tumour_name']
            t.full_clean()
            t.save()
        return t

    def get_package(self):
        package_name = self.data['sortCodingName']
        try:
            pkg = Package.objects.get(name=package_name)
        except ObjectDoesNotExist:
            pkg = Package()
            pkg.save()
        return pkg

    def get_sample(self):
        s = Sample()
        s.ngs_record = self.record
        s.sampletype = self.tissue
        s.patient = self.patient
        s.ammount = self.data['sample_count']
        s.unit = self.data['sample_unit']
        s.sampling_date = self.data['sampling_at']
        s.sampler_remarks = self.data['sampler_remarks']
        s.save()
        return s

    def get_snv(self):
        fmt = pd.read_csv(self.report_fmt, sep='\t', encoding='gbk')
        for ix, row in fmt.iterrows():
            var_dp = int(row['突变深度'])
            if var_dp < 5:
                continue
            s = Snv()
            s.site = self.get_site(row)
            s.sample = self.sample
            s.vf = float(row['突变频率'])
            s.total_dp = int(row['测序深度'])
            s.var_dp = var_dp
            s.mole = row['MOLE']
            s.save()

        annoraw = pd.read_csv(self.annovar_raw, sep='\t', encoding='utf-8',
                              header=self.anno_colnames)
        for ix, row in annoraw.iterrows():
            if row['Chr'] == 'Chr':
                continue
            site = self.get_site(row)
            vf = float(re.search('AF=([\d\.]+)', row['varinfo']).group(1))
            var_dp = int(re.search('DP=([\d]+)', row['varinfo']).group(1))
            mole = int(re.search('MOLE=([\d]+)', row['varinfo']).group(1))
            total_dp = int(var_dp / vf)
            if var_dp < 5:
                continue
            s = Snv.objects.get(site=site, sample=self.sample, vf=vf,
                                total_dp=total_dp, var_dp=var_dp, mole=mole)
            s.fathmm = row['FATHMM_pred']
            s.pp2_hdiv = row['Polyphen2_HDIV_pred']
            s.pp2_hvar = row['Polyphen2_HVAR_pred']
            s.lrt = row['LRT_pred']
            s.muta = row['MutationTaster_pred']
            s.muas = row['MutationAssessor_pred']
            s.radial_svm = row['RadialSVM_pred']
            s.lr = row['LR_pred']
            s.save()

    def get_gene(self, gene):
        try:
            g = Gene.objects.get(name=gene)
        except ObjectDoesNotExist:
            g = Gene()
            g.name = gene
            g.save()
        return g

    def get_site(self, row):
        try:
            s = Site.objects.get(chrom=row['Chr'], start=row['Start'],
                                 end=row['End'], ref=row['Ref'], alt=row['Alt'])
        except ObjectDoesNotExist:
            s = Site()
            s.chrom = row['Chr']
            s.start = row['Start']
            s.end = row['End']
            s.ref = row['Ref']
            s.alt = row['Alt']
            s.gene = self.get_gene(row['基因名称'])
            s.nm_id = row['NM号']
            s.exon_num = row['外显子'].strip('exon')
            s.canno = row['编码序列变异']
            s.panno = row['氨基酸变异']
            s.var_type = row['突变类型']
            s.cosmic = row['COSMIC_ID']
            kgmaf = row['千人突变频率']
            s.kgmaf = float(kgmaf) if kgmaf != '.' else float(0)
            s.rs_id = row['rs_num']
            s.save()
        return s
