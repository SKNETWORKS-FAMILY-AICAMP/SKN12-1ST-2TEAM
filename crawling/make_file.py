import pandas as pd
import os
import pandas as pd

class Make_File:
    def make_file(self):
        if self.file_extensions == 'csv':
            self.df.to_csv(f'data/{self.file_name}.csv', index=False)
            print('csv파일 생성완료')
        elif self.file_extensions == 'xlsx':
            self.df.to_excel(f'data/{self.file_name}.xlsx', index=False)
            print('xlsx파일 생성완료')
        else:
            print('지원하지 않는 확장자명 입니다.')

    def __init__(self, df, file_extensions, file_name):
        self.df = df
        self.file_extensions = file_extensions.lower()
        self.file_name = file_name