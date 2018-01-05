if [[ $# != 1 ]]; then
    #statements
    echo "sh $0 <all.qc.xls>";
    exit -1;
fi
qc=$1;
source /lustre/project/og03/Galaxy/OGSManage/.venv/bin/activate;
python /lustre/project/og03/Galaxy/OGSManage/squery/qcFileParse.py $qc;
deactivate;