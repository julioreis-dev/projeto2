import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


class Inverterfilter:
    def __init__(self, files):
        self.files = files

    def filter(self):
        wb = Workbook()
        number = 0
        for n in self.files:
            label = n[-22:-4]
            df = pd.read_csv(n)
            df_read = df.loc[df['COMS STATUS'] == 255]
            del df_read['ACTIVE POWER']
            if not df_read.empty:
                wb.create_sheet(label)
                ws = wb.get_sheet_by_name(label)
                df_read = pd.DataFrame(df_read, columns=['EQUIPAMENTO', 'timestamp', 'COMS STATUS'])
                df_read = df_read.fillna(label)
                for r in dataframe_to_rows(df_read, index=False, header=True):
                    ws.append(r)
                ws['f2'] = df_read.shape[0]
                number += 1
        wb.save('teste1.xlsx')
