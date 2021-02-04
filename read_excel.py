import pandas as pd
import numpy as np
from io import StringIO

class Shift_read():
    def __init__(self,Shift_excel="Book1.xlsx", Shift_name="Sheet1", emp_num=10, work_day= 30):
        self.Shift_excel = Shift_excel
        self.Shift_name = Shift_name
        self.emp_num = emp_num
        self.work_day = work_day
        #読み込み
        self.read_df = self.read_file()
        self.df_emp = self.read_file_emp()
        self.df_need_person = self.read_need_person_file()
        self.df_Shift = self.read_file_Shift()
        
    #テーブル
    def read_file(self):
        df_1 = pd.read_excel(self.Shift_excel,sheet_name=self.Shift_name)
        #テーブルの範囲
        df = df_1.iloc[4:(4+self.emp_num+3),1:(1+self.work_day+2)]
        df = df.fillna(False)
        df = df.replace("○",True)
        df = df.replace("◎",1)
        return df
    
    #管理人かどうか(全従業員)    
    def read_file_emp(self):
        df_emp = self.read_df.iloc[0:self.emp_num,0:1] 
        df_emp.reset_index(drop=True, inplace=True)
        return df_emp
    
    #必要人数
    def read_need_person_file(self):
        df_need_person = self.read_df.iloc[self.emp_num:(self.emp_num+1),1:(1+self.work_day)]
        df_need_person.reset_index(drop=True, inplace=True)
        df_need_person = df_need_person.T
        df_need_person.reset_index(drop=True, inplace=True)
        return df_need_person
    
        #シフトだけにする
    def read_file_Shift(self):
        df_Shift = self.read_df.iloc[0:self.emp_num,1:(1+self.work_day)]
        df_Shift.reset_index(drop=True, inplace=True)
        df_Shift = df_Shift.T
        df_Shift.reset_index(drop=True, inplace=True)
        df_Shift["必要人数"] = self.df_need_person
        return df_Shift
    
    #管理人であるかの
    def manager(self):
        manager = []
        emp = self.df_emp.values
        for i in range(len(emp)):
            if emp[i]==1:
                manager.append(i)
        return manager
    