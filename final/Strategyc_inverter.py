import pandas as pd
from openpyxl import Workbook
from strategy import Strategy as st


class InverterFilter(st):

    def __init__(self, files):
        super().__init__(self, files, hr=0, minute=0, listequip=None, listocurr=None, listtime=None, listporc=None)

    def filter(self):
        wb = Workbook()
        number = 0
        total_files = len(self.ocurr)
        dataslist = []
        for n in self.ocurr:
            label = n[-22:-4]
            df = pd.read_csv(n)
            df_read = df.loc[df['COMS STATUS'] == 255]
            del df_read['ACTIVE POWER']
            if not df_read.empty:
                alldatas = st.formatcontent(self, wb, label, df_read)
                dataslist = st.listdata(self, alldatas[0], alldatas[1], alldatas[2], alldatas[3])
                number += 1
        st.report(wb, dataslist[0], dataslist[1], dataslist[2], dataslist[3])
        wb.save('teste1.xlsx')
        wb.close()
        print('{}/{} Inversores possuem registro de indisponibilidade.'.format(number, total_files))
