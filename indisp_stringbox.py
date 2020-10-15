import pandas as pd


class Boxfilter:
    def __init__(self, files):
        self.files = files

    def filter(self):
        for n in self.files:
            label = n[-28:-4]
            df = pd.read_csv(n)
            df_read = df.loc[df['COMS STATUS'] == 255]
            del df_read['Current']
            del df_read['Power']
            if not df_read.empty:
                df_read = pd.DataFrame(df_read, columns=['timestamp', 'COMS STATUS', 'EQUIPAMENTO'])
                df_read = df_read.fillna(label)
                print(df_read)
