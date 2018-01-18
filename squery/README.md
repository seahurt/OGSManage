# How to run server？
* open a tmux shell
* activate the virtual env `source /lustre/project/og03/Galaxy/OGSManage/.venv/bin/activate`
* runserver `python manage.py runserver 0:9111`
* put the tmux to background `ctrl + b d`

# How to update database info to include new data?
* scanFile.py
* parseScaned.py


# How to export all data in the database？
* exportDB.py
* exportDB.sh
* exportCfg.py


# How to find out outdated data？
* findNewData.py
* markOutDateStatus.py


# How to find patient name based on OG ID？
* findName.py


# How to save qc to database？
* qcFileParse.py
* QCsave.sh


# How to delete all the data in the database？(if you want to rebuild it from ground)
* emptyDB.py could delete all the record in db

