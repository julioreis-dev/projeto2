import os
import re
import pandas as pd
from threading import Thread
from time import time


def catalogfiles(directory):
    listfileinv = []
    listfilebox = []
    listequip = ['INVERTER', 'STRING BOX']
    lista_arquivos = os.listdir(directory)
    for typequip in listequip:
        for contents in lista_arquivos:
            if re.search('\\b' + typequip + '\\b', contents, re.IGNORECASE):
                contentpath = os.path.join(directory, contents)
                if os.path.isfile(contentpath):
                    if typequip == 'INVERTER':
                        listfileinv.append(contentpath)
                    else:
                        listfilebox.append(contentpath)

    return listfileinv, listfilebox


def inverterfilter(files):
    for n in files:
        label = n[-22:-4]
        df = pd.read_csv(n)
        df_read = df.loc[df['COMS STATUS'] == 255]
        del df_read['ACTIVE POWER']
        if not df_read.empty:
            df_read = pd.DataFrame(df_read, columns=['timestamp', 'COMS STATUS', 'EQUIPAMENTO'])
            df_read = df_read.fillna(label)
            print(df_read)


def boxfilter(files):
    for n in files:
        label = n[-28:-4]
        df = pd.read_csv(n)
        df_read = df.loc[df['COMS STATUS'] == 255]
        del df_read['Current']
        del df_read['Power']
        if not df_read.empty:
            df_read = pd.DataFrame(df_read, columns=['timestamp', 'COMS STATUS', 'EQUIPAMENTO'])
            df_read = df_read.fillna(label)
            print(df_read)


def executiontime(*args):
    execution = args[0] - args[1]
    hr = execution // 3600
    if hr == 0:
        minute = execution // 60
        seg = round((execution % 60) // 1, 2)
    else:
        resthr = execution % 3600
        minute = resthr // 60
        seg = round((minute % 60) // 1, 2)
    return 'Tempo de execução da aplicação: {} hs : {} min : {} seg\nProcesso finalizado com sucesso!!!' \
        .format(hr, minute, seg)


def main():
    v0 = time()
    dest = r'C:\convert\saida\sol do futuro\2020-06-01_2020-07-31'
    filestotal = catalogfiles(dest)
    t1 = Thread(target=inverterfilter, args=(filestotal[0],))
    t1.start()
    t2 = Thread(target=boxfilter, args=(filestotal[1],))
    t2.start()
    t2.join()
    v1 = time()
    tm = executiontime(v1, v0)
    print(tm)


if __name__ == '__main__':
    main()
