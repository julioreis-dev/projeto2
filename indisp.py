import os
import re
import pandas as pd
from threading import Thread


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


def main():
    dest = r'C:\convert\saida\juazeiro\2020-01-01_2020-12-31'
    filestotal = catalogfiles(dest)
    t1 = Thread(target=inverterfilter, args=(filestotal[0],))
    t1.start()
    t2 = Thread(target=boxfilter, args=(filestotal[1],))
    t2.start()


if __name__ == '__main__':
    main()
