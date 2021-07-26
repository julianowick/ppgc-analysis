import os
import filter
import merge
import sucupira

ppgs = [
    {
        "CD_PROGRAMA_IES": "25001019004P6", 
        "ENTIDADE_ENSINO": "UFPE", 
        "PROGRAMA": "CIÊNCIAS DA COMPUTAÇÃO",
        "ACRONYM": "CIn"
    },
    {
        "CD_PROGRAMA_IES": "31001017004P3", 
        "ENTIDADE_ENSINO": "UFRJ", 
        "PROGRAMA": "ENGENHARIA DE SISTEMAS E COMPUTAÇÃO",
        "ACRONYM": "PESC-COPPE"
    },
    {
        "CD_PROGRAMA_IES": "31005012004P9", 
        "ENTIDADE_ENSINO": "PUCRIO", 
        "PROGRAMA": "INFORMÁTICA",
        "ACRONYM": "INF"
    },
    {
        "CD_PROGRAMA_IES": "32001010004P6", 
        "ENTIDADE_ENSINO": "UFMG", 
        "PROGRAMA": "CIÊNCIAS DA COMPUTAÇÃO",
        "ACRONYM": "PPGCC"
    },
    {
        "CD_PROGRAMA_IES": "33002045004P1", 
        "ENTIDADE_ENSINO": "USP-SC", 
        "PROGRAMA": "CIÊNCIAS DA COMPUTAÇÃO E MATEMÁTICA COMPUTACIONAL",
        "ACRONYM": "ICMC"
    },
    {
        "CD_PROGRAMA_IES": "33003017005P8", 
        "ENTIDADE_ENSINO": "UNICAMP", 
        "PROGRAMA": "CIÊNCIA DA COMPUTAÇÃO",
        "ACRONYM": "IC"
    },
    {
        "CD_PROGRAMA_IES": "42001013004P4", 
        "ENTIDADE_ENSINO": "UFRGS", 
        "PROGRAMA": "COMPUTAÇÃO",
        "ACRONYM": "PPGC"
    },
    {
        "CD_PROGRAMA_IES": "42001013078P8", 
        "ENTIDADE_ENSINO": "UFRGS", 
        "PROGRAMA": "MICROELETRÔNICA",
        "ACRONYM": "PGMicro"
    },
    {
        "CD_PROGRAMA_IES": "42005019016P8", 
        "ENTIDADE_ENSINO": "PUCRS", 
        "PROGRAMA": "CIÊNCIA DA COMPUTAÇÃO",
        "ACRONYM": "PPGCC"
    },
    {
        "CD_PROGRAMA_IES": "42007011006P5", 
        "ENTIDADE_ENSINO": "UNISINOS", 
        "PROGRAMA": "COMPUTAÇÃO APLICADA",
        "ACRONYM": "PPGCA"
    },
    {
        "CD_PROGRAMA_IES": "53001010098P3", 
        "ENTIDADE_ENSINO": "UnB", 
        "PROGRAMA": "COMPUTAÇÃO APLICADA",
        "ACRONYM": "PPGI"
    },
]

for ppg in ppgs:
    tmp_files = []
    # filters by PPG ID "producao" and "prod-autor" CSV files for both "artpe" and "anais" publication types
    for file_type in ["producao", "prod-autor"]:
        for prod_type in ["artpe", "anais"]:
            inputfile = f"data/{file_type}-2017a2020-{prod_type}.csv"
            outputfile = f"data/{file_type}-2017a2020-{prod_type}-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}.csv"
            filter.filter_file(inputfile, "CD_PROGRAMA_IES", ppg["CD_PROGRAMA_IES"], outputfile, True)
            tmp_files.append(outputfile)

    # merge filtered files joining "artpe" and "anais" publication types
    for file_type in ["producao", "prod-autor"]:
        basefile = f"data/{file_type}-2017a2020-anais-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}.csv"
        otherfile = f"data/{file_type}-2017a2020-artpe-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}.csv"
        outputfile = f"data/{file_type}-2017a2020-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}.csv"
        merge.merge_files(basefile, otherfile, outputfile, True)

    # create graph from merged files
    authorsfile = f"data/prod-autor-2017a2020-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}.csv"
    papersfile = f"data/producao-2017a2020-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}.csv"
    outputfile = f"data/graph-{ppg['ENTIDADE_ENSINO']}-{ppg['ACRONYM']}-2017-2020.json"
    sucupira.export_graph(authorsfile, papersfile, outputfile)

    # cleaning up
    for f in tmp_files:
        print("Removing temporary file:", f)
        os.remove(f)