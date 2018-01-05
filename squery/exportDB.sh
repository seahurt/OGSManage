#!/bin/bash
if [[ $# != 1 ]]; then
    #statements
    echo "Usage: sh $0 <out.xls>";
    exit 1;
fi
source /lustre/project/og03/Galaxy/OGSManage/.venv/bin/activate &&

python /lustre/project/og03/Galaxy/OGSManage/squery/exportDB.py $1
