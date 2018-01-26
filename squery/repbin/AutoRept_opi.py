#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:
  AutoRept.py  <input_file> <cnv_data> <sample_id> 
  AutoRept.py  <input_file> <cnv_data> <sample_id> [--template_dir=<tmp_dir> --infor=<infor> --cosmic=<cosmic> --outdir=<DIR> --report=<report>]
  AutoRept.py (-h | --help)

Options:
  -h --help                         Show this screen.
  --template_dir=<tmp_dir>          the directory of template report [default: /lustre/project/og03/Public/Pipe/Tumor/Package/Report/lungRept-0.1/datas/].
  --infor=<infor>                   total information tables[default: /lustre/project/og03/Public/Pipe/Tumor/Package/Report/lungRept-0.1/datas/total_info.xlsx].
  --cosmic=<cosmic>                 cosmic file[default: /lustre/project/og03/Public/Pipe/Tumor/DataBase/humandb/Cosmic/V83/CosmicCodingMuts.vcf].
  --outdir=<DIR>                    Output file [default: ./].
  --report=<report>                 choose report manual, default is automatic[default: automatic].
"""


import glob
import xlrd
import time
import os
import re
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from docopt import docopt
from itertools import izip_longest

try:
    from repbin.mailmerge import MailMerge
except ImportError:
    from mailmerge import MailMerge

try:
    from repbin import get_md5_url
except ImportError:
    import get_md5_url

class AutoRept(object):
    '''
    sample information
    '''

    def __init__(self, input_file='', cnv_data='', infor='', cosmic='', sample_id='', outdir='', template_dir='', report = ''):
        super(AutoRept, self).__init__()

        #default automatic
        self.report = report
        #56 genes
        self.ALL_GENES = ['ABL1', 'AKT1', 'ALK', 'APC', 'ARID1A', 'ATM', 'BRAF', 'BRCA1', 'BRCA2', 
            'CDK6', 'CDKN2A', 'CTNNB1', 'DDR2', 'EGFR', 'ERBB2', 'ERBB3', 'ERBB4', 'ESR1', 'FBXW7', 
            'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'HNF1A', 'HRAS', 'IDH1', 'IDH2', 
            'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'MLH1', 'MPL', 'MTOR', 'NF1', 
            'NOTCH1', 'NPM1', 'NRAS', 'NTRK3', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'RICTOR', 
            'ROS1', 'SMAD4', 'SMO', 'SRC', 'TP53', 'TSC2']

        #types of canser in gene_medicine
        self.CANCERS = [u'肺癌', u'甲状腺癌', u'胃肠间质瘤', u'乳腺癌', u'卵巢癌', u'结直肠癌',
            u'膀胱癌', u'黑色素瘤', u'慢性髓细胞白血病', u'神经胶质瘤', u'胃癌']

        #drug of cellule
        self.drug_cellule = u'吉西他滨、长春新碱、铂类药物（顺铂、卡铂）、多柔比星、异环磷酰胺、紫杉醇、伊立替康、依托泊苷'
        
        #cancer hash
        self.hash_genes = {}
        self.hash_genes[u'肺癌基础版'] = ['ALK', 'ERBB2', 'MET', 'PTEN', 'BRAF', 'KRAS', 'NRAS', 'RET', 'EGFR', 
            'MAP2K1', 'PIK3CA', 'ROS1']

        self.hash_genes[u'肺癌标准版'] = ['ALK', 'ERBB2', 'MET', 'PTEN', 'BRAF', 'KRAS', 'NRAS', 'RET', 'EGFR', 
            'MAP2K1', 'PIK3CA', 'ROS1']

        self.hash_genes[u'肺癌高级版'] = ['ABL1', 'AKT1', 'ALK', 'BRAF', 'BRCA1', 'BRCA2', 'CDK6', 'DDR2', 'EGFR', 
            'ERBB2', 'ERBB3', 'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 
            'MET', 'MTOR', 'NRAS', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'ROS1', 'SMO', 'SRC']

        self.hash_genes[u'肺癌全景版'] =  ['ABL1', 'AKT1', 'ALK', 'APC', 'ARID1A', 'ATM', 'BRAF', 'BRCA1', 'BRCA2', 
            'CDK6', 'CDKN2A', 'CTNNB1', 'DDR2', 'EGFR', 'ERBB2', 'ERBB3', 'ERBB4', 'ESR1', 'FBXW7', 
            'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'HNF1A', 'HRAS', 'IDH1', 'IDH2', 
            'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'MLH1', 'MPL', 'MTOR', 'NF1', 
            'NOTCH1', 'NPM1', 'NRAS', 'NTRK3', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'RICTOR', 
            'ROS1', 'SMAD4', 'SMO', 'SRC', 'TP53', 'TSC2']

        self.hash_genes[u'肺癌尊享版'] =  ['ABL1', 'AKT1', 'ALK', 'APC', 'ARID1A', 'ATM', 'BRAF', 'BRCA1', 'BRCA2', 
            'CDK6', 'CDKN2A', 'CTNNB1', 'DDR2', 'EGFR', 'ERBB2', 'ERBB3', 'ERBB4', 'ESR1', 'FBXW7', 
            'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'HNF1A', 'HRAS', 'IDH1', 'IDH2', 
            'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'MLH1', 'MPL', 'MTOR', 'NF1', 
            'NOTCH1', 'NPM1', 'NRAS', 'NTRK3', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'RICTOR', 
            'ROS1', 'SMAD4', 'SMO', 'SRC', 'TP53', 'TSC2']

        self.hash_genes[u'肠癌基础版'] = ['AKT1', 'BRAF', 'EGFR', 'ERBB2', 'KRAS', 'NRAS', 'PIK3CA', 'PTEN']

        self.hash_genes[u'肠癌标准版'] = ['AKT1', 'BRAF', 'EGFR', 'ERBB2', 'KRAS', 'NRAS', 'PIK3CA', 'PTEN']

        self.hash_genes[u'肠癌高级版'] = ['ABL1', 'AKT1', 'ALK', 'BRAF', 'BRCA1', 'BRCA2', 'CDK6', 'DDR2', 'EGFR',
        'ERBB2', 'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'MTOR', 
        'NRAS','PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'ROS1', 'SMAD4', 'SMO', 'SRC']

        self.hash_genes[u'肠癌全景版'] =  ['ABL1', 'AKT1', 'ALK', 'APC', 'ARID1A', 'ATM', 'BRAF', 'BRCA1', 'BRCA2', 
            'CDK6', 'CDKN2A', 'CTNNB1', 'DDR2', 'EGFR', 'ERBB2', 'ERBB3', 'ERBB4', 'ESR1', 'FBXW7', 
            'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'HNF1A', 'HRAS', 'IDH1', 'IDH2', 
            'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'MLH1', 'MPL', 'MTOR', 'NF1', 
            'NOTCH1', 'NPM1', 'NRAS', 'NTRK3', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'RICTOR', 
            'ROS1', 'SMAD4', 'SMO', 'SRC', 'TP53', 'TSC2']

        self.hash_genes[u'肠癌尊享版'] =  ['ABL1', 'AKT1', 'ALK', 'APC', 'ARID1A', 'ATM', 'BRAF', 'BRCA1', 'BRCA2', 
            'CDK6', 'CDKN2A', 'CTNNB1', 'DDR2', 'EGFR', 'ERBB2', 'ERBB3', 'ERBB4', 'ESR1', 'FBXW7', 
            'FGFR1', 'FGFR2', 'FGFR3', 'FLT3', 'GNA11', 'GNAQ', 'HNF1A', 'HRAS', 'IDH1', 'IDH2', 
            'JAK1', 'JAK2', 'KDR', 'KIT', 'KRAS', 'MAP2K1', 'MET', 'MLH1', 'MPL', 'MTOR', 'NF1', 
            'NOTCH1', 'NPM1', 'NRAS', 'NTRK3', 'PDGFRA', 'PIK3CA', 'PTEN', 'RAF1', 'RET', 'RICTOR', 
            'ROS1', 'SMAD4', 'SMO', 'SRC', 'TP53', 'TSC2']

        #report hash
        #u'肺癌基础版.docx' set default
        #u'肺癌高级版.docx'

        #table 3.1
        self.NOT_EXISTS = u'无用药相关基因突变检出'
        self.EXISTS = u'有用药相关基因突变检出'
        self.FLAG_TABLE = {}
        for gene in self.ALL_GENES:
            self.FLAG_TABLE[gene] = self.NOT_EXISTS

        self.outdir = outdir

        self.first_consignor = ''
        self.first_report_num = ''
        self.report_date = ''
        self.patient_name = ''
        self.gender = ''
        self.age = ''
        self.patient_id = ''
        self.clinical_diagnosis = ''
        self.sample_style = ''
        self.sample_id = self.get_id(sample_id)
        self.check_hospital = ''
        self.collection_date = ''
        self.receive_date = ''
        self.sortCodingName = ''

        if self.sample_id:
            self.load_sample()

        #start parse

        self.check_outdir(self.outdir) 
        self.parse(input_file, cnv_data, infor, cosmic, outdir)
        self.transition(template_dir)

    def parse(self,input_file, cnv_data, infor, cosmic, outdir):
        #init genes and type of report
        default_cancer = ['ALK', 'ERBB2', 'MET', 'PTEN', 'BRAF', 'KRAS', 'NRAS', 'RET', 'EGFR', 
            'MAP2K1', 'PIK3CA', 'ROS1']

        self.sortCodingName = self.sortCodingName if self.report == u'automatic' else self.report.decode('utf-8')
        self.MAIN_CANCER, self.REPORT_TYPE = self.__parse_type(self.sortCodingName)
        self.report_name = self.MAIN_CANCER+self.REPORT_TYPE
        self.NEED_GENE = self.hash_genes.get(self.report_name, default_cancer) 
        #靶向药物相关基因检测结果
        #table 核苷酸变异分析结果
        #items:|gene_anno|anno_type|canno|panno|gene_vf|
        self.anno_head = 'gene_anno'
        self.anno_items = []
        #table 拷贝数变异分析结果
        #items:|gene_cnv|start_cnv|end_cnv|
        self.cnv_head = 'gene_cnv'
        self.cnv_items = []

        #table 靶向药物用药提示
        #items:|gene|check_result|FDA-CFDA_drug|FDA-CFDA_other|potential_drug|
        self.rs_nums = {}
        self.table_head = 'gene'
        self.table_items = []

        #key is cosmic
        self.cosmic_table = {}
        if os.path.exists(cosmic):
            self.load_cosmic(cosmic)

        #key is gene+cosmic id
        self.index_table_COSM = {}
        #key is gene+c_anno+mutation
        self.index_table_AM = {}
        if os.path.exists(infor):
            self.load_gene_to_medicine(infor)

        if os.path.exists(input_file):
            self.load_result_gene(input_file)

        if os.path.exists(cnv_data):
            self.load_cnv_tumor(cnv_data)

        #choose to report type(normal or KRAS or feminine) by self.table_items
        #pass chemo report
        if not u'肿瘤化疗' in self.report_name:
            if not self.table_items:
                self.report_name += u'阴性'
            else:
                for table_item in self.table_items:
                    if (table_item.get('gene', None) == 'KRAS' 
                        and self.MAIN_CANCER == u'肺癌'):
                        self.report_name += 'KRAS'
                        break

        #4.1 基因突变用药说明
        #items:|muta_gene|muta_exp|use_drug_exp|
        self.muta_head = 'muta_gene'
        self.muta_items = []
        self.literature = {}
        self.cont_lite = ''

        muta_genes = {}
        self.__get_muta_genes(muta_genes)
        if muta_genes:
            self.load_mutation_info(infor, muta_genes)
        if self.literature:
            self.load_literature(infor)
        #update index
        if self.literature:
            self.update_index()


        #table 潜在获益药物信息
        #items:|drug_name|cancer_name|pharmacology_exp|
        self.drug_head = 'drug_name'
        self.drug_items = []
        drug_names = {}
        self.__get_drug_names(drug_names)
        if drug_names:
            self.load_medicine_info(infor, drug_names)

        #table 临床在研靶向药物解析
        #items:|drug_name_english|target|clinic|ntc_num|research_stage|
        self.solid_cancer = 'solid'
        self.clinic_head = 'drug_name_english'
        self.clinic_items = []
        clinic_drugs = {}
        self.__get_clinic_drugs(clinic_drugs)
        if clinic_drugs:
            self.load_clinic_info(infor, clinic_drugs)

        #table 化疗药物相关基因检测结果
        #key is rs_num,value is type
        self.chemo_items = {}
        if self.rs_nums:
            self.load_chemo_info(infor, self.rs_nums)
            self.reload_chemo_info_without_rs(infor)

    def load_cosmic(self, cosmic_file):
        with open(cosmic_file, 'r') as rows:
            for row in rows:
                if len(row) == 0: continue 
                if row[0] == '#': continue
                CHROM, POS, ID, REF, ALT, QUAL, FILTER,INFO = row.split('\t')
                self.cosmic_table[ID] = INFO

    def load_result_gene(self, input_file):
        '''
        Get sample id and medication prompts
        '''
        with open(input_file, 'r') as row_values:
            for i, row_value in enumerate(row_values):
                table_item = {}
                anno_item = {}
                list_row = row_value.split('\t')
                #self.__get_drug(row_value)
                # pass gibberish data
                if len(list_row) < 53 or i == 0:continue

                Chr = list_row[0].strip()
                start = list_row[1].strip()
                ref = list_row[3].strip()
                alt = list_row[4].strip()
                cur_genes = list_row[6].split(";")
                anno_type = list_row[8]
                cur_cosms = self.__get_cosm(list_row[10])
                cur_anno_mut = self.__get_anno_mu_tumor(list_row[9])
                rs_num = list_row[41].strip()
                cur_vf, cur_dp, cur_mutation_num = self.__original_parse(list_row[53])
                pos = "%s:%s" %(Chr, start)
                self.rs_nums[rs_num] = self.geno_typing(ref, alt, cur_vf, pos)
                #use cosmic id to filter
                if cur_cosms:
                    for cur_cosm in cur_cosms:
                        for cur_gene in cur_genes:
                            index_key = cur_gene+cur_cosm
                            for table_item in self.get_index_COSM(index_key, cur_vf):
                                if table_item and not (table_item in self.table_items):
                                    if table_item['gene'] in self.NEED_GENE:
                                        self.table_items.append(table_item)
                                        self.FLAG_TABLE[table_item['gene']] = self.EXISTS

                                        m = re.search('(SNV|deletion|insertion)' , anno_type)
                                        if m:
                                            anno_type = 'SNV' if m.group(1) == 'SNV' else 'InDel'
                                            anno_item = self.__get_anno_item(cur_gene, anno_type, 
                                                cur_cosm,cur_vf)
                                            self.anno_items.append(anno_item)

                #use c_anno+mutation to filter
                elif not self.table_items:
                    for cur_c_anno, cur_mutation in cur_anno_mut:
                        for cur_gene in cur_genes:
                            index_key = cur_gene+cur_c_anno+cur_mutation
                            for table_item in self.get_index_AM(index_key, cur_vf):
                                if table_item and not (table_item in self.table_items):
                                    if table_item['gene'] in self.NEED_GENE:
                                        self.table_items.append(table_item)
                                        self.FLAG_TABLE[table_item['gene']] = self.EXISTS

                                        m = re.search('(SNV|deletion|insertion)' , anno_type)
                                        if m:
                                            anno_type = 'SNV' if m.group(1) == 'SNV' else 'InDel'
                                            anno_item = self.__get_anno_item_simple(cur_gene, anno_type, 
                                                cur_c_anno, cur_mutation, cur_vf)
                                            self.anno_items.append(anno_item)

    def load_cnv_tumor(self, cnv_data):
        #load cnv information
        with open(cnv_data, "r") as f:
            for line_str in f:
                table_row = {}
                table_cnv = {}
                line_list = line_str.split("\t")
                if len(line_list) < 10:continue
                cancer = line_list[1].decode('gbk')
                mutation_type = line_list[2].decode('gbk')
                gene = line_list[3].decode('gbk')
                start = line_list[5].decode('gbk')
                end = line_list[6].decode('gbk')
                FDA_CFDA_drug = line_list[7].strip().replace(',','\n').decode('gbk')
                FDA_CFDA_drug_other = line_list[8].strip().replace(',','\n').decode('gbk')
                clinic_drug = line_list[9].strip().replace(',','\n').decode('gbk')
                drug_resistance = line_list[10].strip().replace(',','\n').decode('gbk')
                if gene == 'gene':continue
                if FDA_CFDA_drug == '-' and drug_resistance == '-':continue
                if cancer == self.MAIN_CANCER:
                    table_row['cancer']= cancer
                    table_row['gene'] = gene
                    table_row['check_result'] = u'拷贝数扩增'
                    table_row['FDA-CFDA_drug'] = FDA_CFDA_drug
                    table_row['FDA-CFDA_other'] = FDA_CFDA_drug_other
                    table_row['clinic_drug'] = clinic_drug
                    table_row['potential_drug'] = drug_resistance

                    table_cnv['gene_cnv']= gene
                    table_cnv['start_cnv']= start
                    table_cnv['end_cnv']= end
                else:
                    table_row['cancer']= cancer
                    table_row['gene'] = gene
                    table_row['check_result'] = u'拷贝数扩增'
                    table_row['FDA-CFDA_drug'] = '-'
                    table_row['FDA-CFDA_other'] = FDA_CFDA_drug +'\n'+FDA_CFDA_drug
                    table_row['clinic_drug'] = '-'
                    table_row['potential_drug'] = drug_resistance

                    table_cnv['gene_cnv']= gene
                    table_cnv['start_cnv']= start
                    table_cnv['end_cnv']= end

                self.table_items.append(table_row)
                self.cnv_items.append(table_cnv)

    def load_sample(self):
        '''
        Get patient information
        '''
        sample = get_md5_url.SampleInfo(self.sample_id)
        try:
            if sample.data.has_key('data'):
                patient = sample.data['data']
                self.first_consignor = patient['name']
                self.first_report_num = self.sample_id + '-T'
                self.report_date = time.strftime("%Y-%m-%d", time.localtime())
                self.patient_name = patient['name']
                self.gender = patient['gender']
                self.age = patient['age']
                self.patient_id = patient['ID_number']
                self.clinical_diagnosis = patient['tumour_name']
                #get many sample_type
                list_style = [style['sample_type'] for style in patient['sample_list']]
                self.sample_style = u'、'.join(list_style)
                self.check_hospital = patient['hospital']
                self.collection_date = self.__format_date(patient['sample_list'][0]['sampling_at'])
                self.receive_date = self.__format_date(patient['sample_receive_at'])
                self.sortCodingName = patient['sortCodingName']
        except ValueError:
            print "NOT FOUND OG ID:%s" % self.sample_id

    def load_gene_to_medicine(self, infor=None):
        #items:|gene|check_result|FDA-CFDA_drug|FDA-CFDA_other|potential_drug|
        index_table_COSM = {}
        index_table_AM = {}

        data = xlrd.open_workbook(infor)
        #sheet:'gene_medicine'
        table = data.sheets()[0]
        nrows = table.nrows
        for i in xrange(nrows):
            index_cancer = table.row_values(i)[0].strip()
            index_gene = table.row_values(i)[1].strip().upper()
            index_c_anno = table.row_values(i)[2].strip().upper()
            index_mutation = table.row_values(i)[3].strip().upper()
            index_cosm = table.row_values(i)[5].strip().upper()
            if(index_gene=='-' or index_cosm=='-' or (not index_gene) or (not index_cosm)):
                pass
            else:
                index_key = index_cancer+index_gene+index_cosm
                index_table_COSM.setdefault(index_key, table.row_values(i))

            if(index_gene=='-' or index_c_anno=='-' or index_mutation =='-'
                or (not index_gene)  or (not index_c_anno) or (not index_mutation)):
                pass
            else:
                index_key = index_cancer+index_gene+index_c_anno+index_mutation
                index_table_AM.setdefault(index_key, table.row_values(i))

        self.index_table_COSM = index_table_COSM
        self.index_table_AM = index_table_AM

    def load_mutation_info(self, tatol_info, muta_genes):
        #items:|muta_gene|muta_exp|use_drug_exp|

        muta_items = []
        literature = {}
        data = xlrd.open_workbook(tatol_info)
        #sheet:'cancer_mutation_gene_info':
        table = data.sheets()[1]
        nrows = table.nrows
        index_order = 1
        for i in xrange(nrows):
            muta_table = {}
            muta_gene = table.row_values(i)[0].strip().upper()
            muta_exp = table.row_values(i)[1]
            use_drug_exp = table.row_values(i)[2]
            if muta_gene in muta_genes:
                muta_table['muta_gene'] = "%s\n%s" % (muta_gene, muta_genes[muta_gene])
                muta_table['muta_exp'] = muta_exp
                muta_table['use_drug_exp'] = use_drug_exp

                #get index of literature
                for  indexs in re.findall(r'\[(.*?)\]',use_drug_exp):
                    for index in self.__format_index(indexs):
                        if index not in literature:
                            literature[int(index)] = index_order
                            index_order += 1
                muta_items.append(muta_table)

        self.literature = literature
        self.muta_items = muta_items
        return

    def update_index(self):
        index_map = self.literature
        for muta_table in self.muta_items:
             exp = muta_table['use_drug_exp'].encode('utf-8')
             muta_table['use_drug_exp'] = self.__update_index(exp, index_map)

    def __update_index(self, exp, hash):
        indexs = re.finditer(r'\[(.*?)\]', exp)
        new_exp = exp[:]
        for index in indexs:
            start = index.start()
            end = index.end()
            whole_nums = index.group(0)
            str_nums = index.group(1)
            re_cont = u''
            if '-' in str_nums and ',' in str_nums:
                re_cont = u''
            elif '-' in str_nums:
                se = str_nums.split('-')
                first_val = min(hash[int(se[0])], hash[int(se[1])])
                second_val = max(hash[int(se[0])], hash[int(se[1])])
                re_cont = u'【%d-%d】' % (first_val, second_val) if len(se) == 2 else ''
            elif ',' in str_nums:
                hash_nums = sorted([hash[int(str_num)] for str_num in str_nums.split(',')])
                re_cont = u','.join(map(str,hash_nums))
                re_cont = u'【' + re_cont + u'】'
            else:
                if str_nums.isdigit():
                    re_cont = u'【' + ('%d' % (hash[int(str_nums)])) + u'】'
                else:
                    re_cont = u''
            new_exp = new_exp.replace(whole_nums, re_cont, 1)
        return new_exp

    def load_literature(self, tatol_info):
        pos_cont_lite = {}
        data = xlrd.open_workbook(tatol_info)
        #sheet:'references':
        table = data.sheets()[2]
        nrows = table.nrows
        for i in xrange(nrows):
            index = table.row_values(i)[0]
            name = table.row_values(i)[1]
            title = table.row_values(i)[2]
            my_date = table.row_values(i)[3]
            if index in self.literature:
                pos_num = self.literature[index]
                pos_cont_lite[pos_num] = "%d.    %s.%s.%s\n" % (pos_num, name, title, my_date)
        for key, value in sorted(pos_cont_lite.items(), key=lambda item:item[0]):
            self.cont_lite += value
        return

    def load_medicine_info(self, tatol_info, drug_names):
        drug_items = []
        data = xlrd.open_workbook(tatol_info)
        #sheet:'cancer_medicine_info':
        table = data.sheets()[3]
        nrows = table.nrows
        for i in xrange(nrows):
            drug_item = {}
            drug_name = table.row_values(i)[2]
            drug = table.row_values(i)[5]
            cancer = table.row_values(i)[6]
            exp = table.row_values(i)[7]
            if drug_name in drug_names:
                drug_item['drug_name'] = drug
                drug_item['cancer_name'] = cancer
                drug_item['pharmacology_exp'] = exp
                drug_items.append(drug_item)
        self.drug_items = drug_items
        return

    def load_clinic_info(self, tatol_info, clinic_drugs):
        clinic_items = []
        data = xlrd.open_workbook(tatol_info)
        #sheet:'clinic_medicine_info':
        table = data.sheets()[4]
        nrows = table.nrows
        #items:|drug_name_english|target|clinic|ntc_num|research_stage|
        for i in xrange(nrows):
            drug_item = {} 
            cancer = table.row_values(i)[0].strip()
            drug_name_english = table.row_values(i)[1].strip()
            target = table.row_values(i)[2]
            clinic = table.row_values(i)[3]
            ntc_num = table.row_values(i)[4]
            research_stage = table.row_values(i)[5]
            if ((cancer == self.MAIN_CANCER or cancer == self.solid_cancer) and
                drug_name_english in clinic_drugs):
                drug_item['drug_name_english'] = drug_name_english
                drug_item['target'] = target
                drug_item['clinic'] = clinic
                drug_item['ntc_num'] = ntc_num
                drug_item['research_stage'] = research_stage
                clinic_items.append(drug_item)
        self.clinic_items = clinic_items
        return


    def load_chemo_info(self, tatol_info, table_rs):
        data = xlrd.open_workbook(tatol_info)
        #sheet:'chemotherapy_drug2':
        table = data.sheets()[5]
        nrows = table.nrows
        chemo_items = {} 
        for i in xrange(nrows):
            drug = table.row_values(i)[0].strip().encode('utf-8')
            rs_num = table.row_values(i)[2].strip().encode('utf-8')
            genoty = table.row_values(i)[6].strip().encode('utf-8')
            infor = table.row_values(i)[7].strip().encode('utf-8')
            if(rs_num in table_rs and table_rs[rs_num] == genoty):
                chemo_items[u'%s_%s_1' %(rs_num, drug)] = genoty
                chemo_items[u'%s_%s_2' %(rs_num, drug)] = u'%s' % infor
        self.chemo_items = chemo_items
        return

    def reload_chemo_info_without_rs(self, tatol_info):
        data = xlrd.open_workbook(tatol_info)
        #sheet:'chemotherapy_drug2':
        table = data.sheets()[5]
        nrows = table.nrows
        chemo_items_wd = {}
        for i in xrange(nrows):
            drug = table.row_values(i)[0].strip().encode('utf-8')
            rs_num = table.row_values(i)[2].strip().encode('utf-8')
            genoty = table.row_values(i)[6].strip().encode('utf-8')
            infor = table.row_values(i)[7].strip().encode('utf-8')
            mutation = table.row_values(i)[8].strip().encode('utf-8')
            key_1 = u'%s_%s_1' %(rs_num, drug)
            key_2 = u'%s_%s_2' %(rs_num, drug)
            if mutation == u'WT' and not key_1 in self.chemo_items:
                chemo_items_wd[key_1] = genoty
                chemo_items_wd[key_2] = u'%s' % infor
        self.chemo_items.update(chemo_items_wd)
        return

    def get_index_COSM(self, index_key, cur_matation_per):
        '''
        Get medication prompts from infor
        '''
        table_rows = []
        key = self.MAIN_CANCER+index_key
        if self.index_table_COSM.has_key(key):
            table_row = self.get_table_row(key, cur_matation_per)
            if table_row:
                table_rows.append(table_row)
                #delete repeated gene
                for cancer in self.CANCERS:
                    self.__delete_key(self.MAIN_CANCER, index_key)
        else:
            check_table = {}
            copy_cancers = self.CANCERS[:]
            if self.MAIN_CANCER in copy_cancers:
                copy_cancers.remove(self.MAIN_CANCER)
            for monior_cancer in self.CANCERS:
                key_monior = monior_cancer + index_key
                if self.index_table_COSM.has_key(key_monior):
                    table_row = self.get_table_row(key_monior, cur_matation_per, check_table)
                    if table_row:
                        check_table[table_row['gene']+table_row['check_result']] = table_row
                        self.__delete_key(monior_cancer, index_key)
            for key,table_row in check_table.iteritems():
                table_rows.append(table_row)
        return table_rows

    def get_index_AM(self, index_key, cur_matation_per):
        '''
        Get medication prompts from infor
        '''
        table_rows = []
        key = self.MAIN_CANCER+index_key
        if self.index_table_AM.has_key(key):
            table_row = self.get_table_row(key, cur_matation_per) 
            table_rows.append(table_row)
            #not need minor
            for cancer in self.CANCERS:
                del_key  = cancer + index_key
                if del_key in self.index_table_AM:
                    del self.index_table_AM[del_key]
        else:
            check_table = {}
            copy_cancers = self.CANCERS[:]
            if self.MAIN_CANCER in copy_cancers:
                copy_cancers.remove(self.MAIN_CANCER)
            for monior_cancer in self.CANCERS:
                key_monior = monior_cancer+index_key
                if self.index_table_COSM.has_key(monior_cancer+index_key):
                    table_row = self.get_table_row(key_monior, cur_matation_per, check_table)
                    if table_row:
                        check_table[table_row['gene']+table_row['check_result']] = table_row
                        del self.index_table_AM[key_monior]
            for key,table_row in check_table.iteritems():
                table_rows.append(table_row)
        return table_rows

    def __get_anno_mu_tumor(self, line_str=""):
        lines=[]
        line_list = line_str.split(';')
        for items in line_list:
            if items:
                items_list = items.split(':')
                if len(items_list) < 5:
                    continue
                anno, mas = items_list[3].strip().upper(), items_list[4].strip().upper()
                #format anno
                pattern = re.compile(r'c.([a-zA-Z])(\d+)([a-zA-Z])',re.I)
                match = pattern.match(anno)
                if match:
                    if all(match.groups()):
                        anno = "C.%s%s>%s" % (match.group(2), match.group(1), match.group(3))
                lines.append((anno, mas))
        return lines

    def __get_drug(self, line_str = ""):
        filename = unicode(self.sample_id)+self.report_name+u'_drug.xls'
        output_file = os.path.join(self.outdir, filename.encode('utf-8'))
        line = line_str.split('\t')
        with open(output_file,'a') as f:
            if len(line) >= 26:
                gene = line[6].strip().upper()
                CLINSIG = line[12].strip().upper()
                CLNDBN =line[13] .strip().upper()
                if gene in self.NEED_GENE:
                    if ('RESPONSE' in CLINSIG or 'RESPONSE' in CLNDBN
                        or 'RESISTANT' in CLINSIG or 'RESISTANT' in CLNDBN):
                        f.write(line_str)

    def __get_cosm(self, line_str=""):
        '''
        Get cosm from index template
        '''
        line_str = line_str.strip().upper()
        pattern = re.compile(r'(COSM\d+)', re.I)
        return pattern.findall(line_str)



    def __original_parse(self, line_str=""):
        '''
        return cur_vf, cur_dp, cur_mutation_num
        '''
        values = (0.0, 0, 0 )
        if line_str:
            line_list = line_str.split(';')
            if len(line_list) < 4:
                return ""
            values = (float(line_list[0].split('=')[1]),
                    int(line_list[1].split('=')[1]),
                    int(line_list[3].split('=')[1]))
        return values

    def __format_index(self, indexs):
        if '-' in indexs and ',' in indexs:return []
        if '-' in indexs:
            se = indexs.split('-')
            return range(int(se[0]), int(se[1])+1) if len(se) == 2 else []
        elif ',' in indexs:
            return map(int,indexs.split(','))
        else:
            if indexs.isdigit():
                return [int(indexs)]
            else:
                return []

    def __format_date(self, str_date):
        nor_date = ''
        pattern = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})')
        m = pattern.search(str_date)
        if m:
            nor_date = m.group(0)
        return nor_date

    def __get_anno_item(self, cur_gene, anno_type, cur_cosm,cur_vf):
        #items:|gene|anno_type|canno|panno|gene_vf|
        anno_item = {}
        canno = '-'
        panno = '-'

        if cur_cosm in self.cosmic_table:
            INFO = self.cosmic_table[cur_cosm]
            canno = '-'
            panno = '-'
            m = re.search(u'CDS=(.*?);AA=(.*?);',INFO)
            if m:
                canno = m.group(1)
                panno = m.group(2)
        anno_item['gene_anno'] = cur_gene
        anno_item['anno_type'] = anno_type
        anno_item['canno'] = canno
        anno_item['panno'] = panno
        anno_item['gene_vf'] = '%.2f%%' %(float(cur_vf)*100)
        return anno_item

    def __get_anno_item_simple(self, cur_gene, anno_type, canno, panno, cur_vf):
        anno_item = {}
        anno_item['gene_anno'] = cur_gene
        anno_item['anno_type'] = anno_type
        anno_item['canno'] = canno
        anno_item['panno'] = panno
        anno_item['gene_vf'] = '%.2f%%' %(float(cur_vf)*100)
        return anno_item

    def transition(self, target_dir):
        '''
        output information to template of word format
        '''       
        template = os.path.join(unicode(target_dir), self.report_name + u'.docx').encode('utf-8')
        with MailMerge(template) as document:
            
            merge = self.__dict__

            for gene in self.ALL_GENES:
                merge['FLAG_%s'%(gene)] = self.FLAG_TABLE[gene]

            document.merge(**merge)
            document.merge(**self.chemo_items)
            document.merge_rows(self.anno_head, self.anno_items)
            document.merge_rows(self.cnv_head, self.cnv_items)
            document.merge_rows(self.table_head, self.table_items)
            document.merge_rows(self.muta_head, self.muta_items)
            document.merge_rows(self.drug_head, self.drug_items)
            document.merge_rows(self.clinic_head, self.clinic_items)

            filename = (self.sample_id.decode('utf-8') + u'_' + self.patient_name 
                        + u'-' + self.report_name + u'.docx')
            output_file = os.path.join(self.outdir, filename.encode('utf-8'))
            with open(output_file, 'w') as f:
                document.write(f)

    def __new_input(self, table, key, row):
        filename = u'lung_'+self.sample_id.decode('utf-8')+u'_drugmap.xls'
        output_file = os.path.join(self.outdir, filename)
        row[-1] = row[-1].replace("\n","")
        if table.has_key(key):
            cancer = table[key][0].replace("\n",",")
            drug = table[key][8].replace("\n",",")+"\n"
            new_row = "\t".join(row+[cancer, drug])
            with codecs.open(output_file, 'a', encoding='utf-8') as f:
                f.write(new_row)

    def get_table_row(self, key, cur_matation_per, check_table = {}):
        table_row = {}
        cancer = self.index_table_COSM[key][0].strip()
        gene = self.index_table_COSM[key][1].strip()
        check_result = (self.index_table_COSM[key][2] + '\n'
                                     + self.index_table_COSM[key][3] + '\n'
                                     + (u'突变丰度: %.2f%%' % (cur_matation_per * 100))).strip()
        FDA_CFDA_drug = self.index_table_COSM[key][8].replace(',', '\n').strip()
        FDA_CFDA_other = self.index_table_COSM[key][9].replace(',', '\n').strip()
        clinic_drug = self.index_table_COSM[key][10].replace(',', '\n').strip()
        potential_drug = self.index_table_COSM[key][11].replace(',', '\n').strip()

        if((gene+check_result)) not in check_table:
            table_row['cancer'] = cancer
            table_row['gene'] =  gene
            table_row['check_result'] = check_result
            table_row['FDA-CFDA_drug'] = FDA_CFDA_drug
            table_row['FDA-CFDA_other'] = FDA_CFDA_other
            table_row['clinic_drug'] = clinic_drug
            table_row['potential_drug'] = potential_drug

        else:
            table_row['cancer'] = cancer
            table_row['gene'] =  gene
            table_row['check_result'] = check_result
            table_row['FDA-CFDA_drug'] = '-'
            many_other = check_table[(gene+check_result)]['FDA-CFDA_other'] + '\n' +FDA_CFDA_other
            table_row['FDA-CFDA_other'] = '\n'.join(list(set(re.split(r'[,\n]',many_other))))
            table_row['clinic_drug'] = '-'
            table_row['potential_drug'] = '-'

        if table_row['FDA-CFDA_drug'] == '-' and table_row['FDA-CFDA_other'] == '-':
            table_row = {}
        return table_row
    
    def __get_muta_genes(self, muta_genes):
        for item in self.table_items:
            muta = ''
            m = re.search(r'(p\..*?\n|\(CN=[0-9\.]*?\))', item.get('check_result',''), re.I)
            if m:
                muta = m.group(1)
                if muta[:3] == '(CN':
                    muta = u'拷贝数扩增\n'+muta
            if item['gene'] in muta_genes:
                muta_genes[item['gene']] += muta
            else:
                muta_genes[item['gene']] = muta
            self.FLAG_TABLE[item['gene']] = self.EXISTS
        return 

    def __get_drug_names(self, drug_names):
        for item in self.table_items:
            if 'FDA-CFDA_drug'in item:
                for drug in item['FDA-CFDA_drug'].split('\n'):
                    if drug:
                        drug_names[drug] = True
            if  'FDA-CFDA_other' in item:
                for drug in item['FDA-CFDA_other'].split('\n'):
                    if drug:
                        drug_names[drug] = True 

    def __delete_key(self, cancer, index_key):
        COSM_key  = cancer + index_key
        if COSM_key in self.index_table_COSM:
            cont = self.index_table_COSM[COSM_key]
            del self.index_table_COSM[COSM_key]
            AM_key = cancer + cont[2] + cont[3]
            if AM_key in self.index_table_AM:
                del self.index_table_AM[AM_key] 

    def __get_clinic_drugs(self, clinic_drugs):
        for item in self.table_items:
            if 'clinic_drug' in item:
                for clinic_drug in item['clinic_drug'].split('\n'):
                    if clinic_drug == '-':continue
                    clinic_drugs[clinic_drug.strip()] = item['cancer']

                #remove (*) from  clinic_drug
                item['clinic_drug'] = re.sub(r'\(.*?\)','',item['clinic_drug'])


    def __parse_type(self,text):
        s1 = re.search(ur'(肺癌|肿瘤化疗|肠癌)', text)
        cancer = s1.group(1) if s1 else u'肺癌'

        s2 = re.search(ur'(基础版|标准版|高级版|全景版|尊享版)', text)
        report_type = s2.group(1) if s2 else u'基础版'

        #change the drug,if the tyle of sample is not cellule
        s3 = re.search(ur'组织版', text)
        if s3:
            self.drug_cellule = u'吉西他滨、铂类药物（顺铂、卡铂）、紫杉醇、依托泊苷、培美曲塞'

        return cancer, report_type

    def get_id(self, OG):
        m = re.match(r"(\w+\d+)", OG)
        if m:
            OG = m.group(1)
        return OG
        
    def geno_typing(self, ref, alt, vf ,pos):
        low = 0.3
        high = 0.7
        if pos == '2:234668879':
            vf = float(vf)
            if vf < low:
                return '6/6TA'
            elif vf > high:
                return '7/7TA'
            else:
                return '6/7TA'
        else:
            base = {'A', 'G', 'T', 'C'}
            p = re.compile(r'[/|]')
            alts = p.split(alt)
            if not {ref}.union(set(alts)).issubset(base):
                ids = [_x == _y for _x, _y in
                       izip_longest(ref, alt)].index(
                    False)
                ref = ref[ids:]
                alt = alt[ids:]
                if alt == '-':
                    alt = 'del'
                if ref == '-':
                    ref = 'del'
            elif len(alts) > 1:
                if len(p.split(vf)) == 1:
                    vf = p.split(vf) * 2
                vf = [float(_i) for _i in p.split(vf)]
                if vf[0] >= 0.5:
                    if vf[1] >= 0.5:
                        return "{}".format('/'.join(sorted(alts)))
                    else:
                        alt = alts[0]
                        vf = vf[0]
                else:
                    if vf[1] > 0.5:
                        alt = alts[1]
                        vf = vf[1]
                    else:
                        return "{}".format('/'.join([ref, ref]))
            vf = float(vf)
            if vf < 0.3:
                return "{}".format('/'.join([ref, ref]))
            elif vf > 0.7:
                return "{}".format('/'.join([alt, alt]))
            else:
                return "{}".format('/'.join(sorted([ref, alt])))

    def check_outdir(self, dir):
        if os.path.isdir(dir):
            pass
        else:
            os.makedirs(dir)

def main():
    args = docopt(__doc__, version='lungrept.py')
    kwargs = {
        'input_file': os.path.abspath(args['<input_file>']),
        'cnv_data': os.path.abspath(args['<cnv_data>']),
        'infor': os.path.abspath(args['--infor']),
        'cosmic': os.path.abspath(args['--cosmic']),
        'template_dir': os.path.abspath(args['--template_dir']),
        'sample_id': args['<sample_id>'],
        'outdir': os.path.abspath(args['--outdir']),
        'report': args['--report']
    }
    autorept = AutoRept(**kwargs)

if __name__ == '__main__':
    main()
