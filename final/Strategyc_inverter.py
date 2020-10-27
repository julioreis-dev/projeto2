import pandas as pd
from openpyxl import Workbook
from strategy import Strategy


class InverterFilter(Strategy):

    def __init__(self, files):
        super().__init__(files)

    def filter(self):
        wb = Workbook()
        number = 0
        total_files = len(self.files)
        dataslist = []
        for n in self.files:
            label = n[-22:-4]
            df = pd.read_csv(n)
            df_read = df.loc[df['COMS STATUS'] == 255]
            del df_read['ACTIVE POWER']
            if not df_read.empty:
                alldatas = self.formatcontent(wb, label, df_read)
                dataslist = list(self.listdata(alldatas[0], alldatas[1], alldatas[2], alldatas[3]))
                number += 1
        self.report(wb, dataslist[0], dataslist[1], dataslist[2], dataslist[3])
        wb.save('teste1.xlsx')
        wb.close()
        print('{}/{} Inversores possuem registro de indisponibilidade.'.format(number, total_files))
        