import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment, Protection


class InverterFilter:
    def __init__(self, files, ocurr=0, hr=0, minute=0):
        self.files = files
        self.ocurr = ocurr
        self.hr = hr
        self.minute = minute

    def filter(self):
        wb = Workbook()
        number = 0
        for n in self.files:
            label = n[-22:-4]
            df = pd.read_csv(n)
            df_read = df.loc[df['COMS STATUS'] == 255]
            del df_read['ACTIVE POWER']
            if not df_read.empty:
                self.formatcontent(wb, label, df_read)
                number += 1
        print('{} inversores possuem dados de indisponibilidade.'.format(number))
        wb.save('teste1.xlsx')

    def formatcontent(self, wb, label, df_read):
        wb.create_sheet(label)
        ws = wb.get_sheet_by_name(label)
        df_read = pd.DataFrame(df_read, columns=['timestamp', 'COMS STATUS'])
        for r in dataframe_to_rows(df_read, index=False, header=True):
            ws.append(r)
        self.formatsheet(ws, df_read, label)

    def formatsheet(self, ws, df_read, label):
        self.ocurr = df_read.shape[0]
        ws['e2'] = 'Equipamento:'
        ws['e3'] = 'Ocorrencias:'
        ws['e4'] = 'Tempo total:'
        ws['e5'] = '% de indisponibilidade no mês:'
        ws['f2'] = '{}'.format(label)
        ws['f3'] = self.ocurr
        ws['f4'] = self.calctime()
        ws['f5'] = '{}%'.format(round(self.calcporc(), 2))
        ws['f2'].alignment = Alignment(horizontal='left')
        ws['f3'].alignment = Alignment(horizontal='left')
        ws['f4'].alignment = Alignment(horizontal='left')
        ws['f5'].alignment = Alignment(horizontal='left')

    def calctime(self):
        self.hr = (self.ocurr // 4)
        self.minute = (self.ocurr - (self.hr * 4)) * 15
        return '{} hs : {} min : {} seg'.format(self.hr, self.minute, 0)

    def calcporc(self):
        tothr = (31 * 24)
        convhrs = self.minute / 60
        result = ((self.hr + convhrs) * 100) / tothr
        return result
