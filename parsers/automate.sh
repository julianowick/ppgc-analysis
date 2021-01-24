#!/bin/bash
CD_PROGRAMA_IES="42007011006P5"
ENTIDADE_ENSINO="UNISINOS"
PROGRAMA="PPGCA"

/usr/bin/python3 parsers/filter.py data/producao-2017a2020-anais.csv CD_PROGRAMA_IES $CD_PROGRAMA_IES
mv data/producao-2017a2020-anais-filtered.csv data/producao-2017a2020-anais-$CD_PROGRAMA_IES.csv 

/usr/bin/python3 parsers/filter.py data/producao-2017a2020-artpe.csv CD_PROGRAMA_IES $CD_PROGRAMA_IES
mv data/producao-2017a2020-artpe-filtered.csv data/producao-2017a2020-artpe-$CD_PROGRAMA_IES.csv 

/usr/bin/python3 parsers/filter.py data/prod-autor-2017a2020-anais.csv CD_PROGRAMA_IES $CD_PROGRAMA_IES
mv data/prod-autor-2017a2020-anais-filtered.csv data/prod-autor-2017a2020-anais-$CD_PROGRAMA_IES.csv 

/usr/bin/python3 parsers/filter.py data/prod-autor-2017a2020-artpe.csv CD_PROGRAMA_IES $CD_PROGRAMA_IES
mv data/prod-autor-2017a2020-artpe-filtered.csv data/prod-autor-2017a2020-artpe-$CD_PROGRAMA_IES.csv 

/usr/bin/python3 parsers/merge.py data/producao-2017a2020-anais-$CD_PROGRAMA_IES.csv data/producao-2017a2020-artpe-$CD_PROGRAMA_IES.csv
mv data/producao-2017a2020-anais-$CD_PROGRAMA_IES-merged.csv data/producao-2017a2020-$CD_PROGRAMA_IES.csv

/usr/bin/python3 parsers/merge.py data/prod-autor-2017a2020-anais-$CD_PROGRAMA_IES.csv data/prod-autor-2017a2020-artpe-$CD_PROGRAMA_IES.csv
mv data/prod-autor-2017a2020-anais-$CD_PROGRAMA_IES-merged.csv data/prod-autor-2017a2020-$CD_PROGRAMA_IES.csv

/usr/bin/python3 parsers/sucupira.py data/prod-autor-2017a2020-$CD_PROGRAMA_IES.csv data/producao-2017a2020-$CD_PROGRAMA_IES.csv data/graph-$PROGRAMA-$ENTIDADE_ENSINO-2017-2020.json
