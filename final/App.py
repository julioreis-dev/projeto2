import os
import re
import Strategyc_inverter as inv
import Strategyc_stringbox as box
from threading import Thread
from time import time


class Administration:
    def __init__(self, directory):
        self.directory = directory

    def catalogfiles(self):
        listfileinv = []
        listfilebox = []
        listequip = ['INVERTER', 'STRING BOX']
        lista_arquivos = os.listdir(self.directory)
        for typequip in listequip:
            for contents in lista_arquivos:
                if re.search('\\b' + typequip + '\\b', contents, re.IGNORECASE):
                    contentpath = os.path.join(self.directory, contents)
                    if os.path.isfile(contentpath):
                        if typequip == listequip[0]:
                            listfileinv.append(contentpath)
                        else:
                            listfilebox.append(contentpath)
        return listfileinv, listfilebox

    @staticmethod
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
    dest = r'C:\convert\saida\são pedro\2020-01-01_2020-01-31'
    adm = Administration(dest)
    filestotal = adm.catalogfiles()
    aplication = [inv.InverterFilter, box.BoxFilter]
    equip = ['Inversores', 'Stringbox']
    for index, app in enumerate(aplication):
        manage = app(filestotal[index])
        t1 = Thread(target=manage.filter)
        t1.start()
        print('Início do processo {} - Analisando {}............'.format(index+1, equip[index]))
        if index == 1:
            t1.join()
    v1 = time()
    tm = adm.executiontime(v1, v0)
    print(tm)


if __name__ == '__main__':
    main()
