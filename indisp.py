import os
import re
import indisp_inverter as inv
import indisp_stringbox as box
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
    dest = r'C:\convert\saida\juazeiro\2020-02-01_2020-02-29'
    filestotal = catalogfiles(dest)
    manage = inv.InverterFilter(filestotal[0])
    t1 = Thread(target=manage.filter)
    t1.start()
    manage2 = box.BoxFilter(filestotal[1])
    t2 = Thread(target=manage2.filter)
    t2.start()
    t2.join()
    v1 = time()
    tm = executiontime(v1, v0)
    print(tm)

if __name__ == '__main__':
    main()
