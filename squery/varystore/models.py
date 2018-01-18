from django.db import models
from samplequery.models import Record, Tissues
from repbin import get_md5_url
# Create your models here.


class Tumor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Gene(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    ensg_id = models.CharField(max_length=100, default='')
    hgnc_id = models.CharField(max_length=100, default='')
    entrez_id = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.symbol


class Site(models.Model):
    chrom = models.CharField(max_length=2)
    start = models.CharField(max_length=15)
    end = models.CharField(max_length=15)
    ref = models.CharField(max_length=1000)
    alt = models.CharField(max_length=1000)
    gene = models.ForeignKey(Gene, on_delete=models.CASCADE)
    nm_id = models.CharField(max_length=100)
    exon_num = models.IntegerField()
    canno = models.CharField(max_length=100)
    panno = models.CharField(max_length=100)
    var_type = models.CharField(max_length=100)
    cosmic = models.CharField(max_length=20, default='.')
    kgmaf = models.FloatField(default=0)
    rs_id = models.CharField(max_length=20, default='.')

    def __str__(self):
        return ','.join([self.chrom, self.start, self.end, self.gene])


class Drug(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Package(models.Model):
    """
        init gene befor this
        init tumor before this
    """
    name = models.CharField(max_length=100)
    tumor = models.ForeignKey(Tumor, on_delete=models.CASCADE,
                              default=None)
    gene = models.ManyToManyField(Gene)

    def __str__(self):
        return self.name


class Patient(models.Model):
    SEX = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    id_number = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=SEX)
    tumor_type = models.ForeignKey(Tumor, on_delete=models.CASCADE)
    hospital = models.CharField(max_length=100)
    service_package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sample(models.Model):
    ngs_record = models.OneToOneField(Record, on_delete=models.CASCADE)
    sampletype = models.ForeignKey(Tissues, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ammount = models.IntegerField()
    unit = models.CharField(max_length=10)
    sampling_date = models.DateField()
    sampler_remarks = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.ngs_record

    @property
    def signature(self):
        f = get_md5_url.SampleInfo(self.ngs_record.og_id)
        return f.get_md5

    @property
    def retrieveinfo(self):
        f = get_md5_url.SampleInfo(self.ngs_record.og_id)
        return f.data


class Snv(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    vf = models.FloatField()
    total_dp = models.IntegerField()
    var_dp = models.IntegerField()
    mole = models.IntegerField()
    fathmm = models.CharField("FATHMM_prediction", max_length=1, default='.')
    pp2_hdiv = models.CharField("Polyphen2_HDIV_pred", max_length=1, default='.')
    pp2_hvar = models.CharField("Polyphen2_HVAR_pred", max_length=1, default='.')
    lrt = models.CharField("LRT_pred", max_length=1, default='.')
    muta = models.CharField("MutationTaster_pred", max_length=1, default='.')
    muas = models.CharField("MutationAssessor_pred", max_length=1, default='.')
    radial_svm = models.CharField("RadialSVM_pred", max_length=1, default='.')
    lr = models.CharField("LR_pred", max_length=1, default='.')


class Cnv(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    copynum = models.FloatField()
    fragnum = models.IntegerField()
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)


class DrugRecord(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    cancer = models.ForeignKey(Tumor, on_delete=models.CASCADE)
    drug = models.ManyToManyField(Drug)
