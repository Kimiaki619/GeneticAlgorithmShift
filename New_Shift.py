import pandas as pd
import numpy as np
from pulp import *
from ortoolpy import addvars, addbinvars
from io import StringIO

class new_Shift():
    def __init__(self,df_Shift,manager):
        self.df_Shift = df_Shift
        self.L_manager = manager
        self.need()
        self.C()
        #数理モデル
        self.m = LpProblem(sense=LpMinimize)
        self.V()
        
    def need(self):
        self.n_koma = self.df_Shift.shape[0]
        self.n_emp = self.df_Shift.shape[1]-1
        self.L_emp = list(range(self.n_emp))
    
    def C(self,C_need_person = 10,C_not_hope = 100,C_least_Shift = 1,C_need_manager = 100,C_1day_2 = 10):
        #必要人数
        self.C_need_person = C_need_person
        #希望するシフトに入れない
        self.C_not_hope = C_not_hope
        #希望するシフトに半分は入れるようにする
        self.C_least_Shift = C_least_Shift
        #マネージャーが必要は必要
        self.C_need_manager = C_need_manager
    
    def V(self):
        #該当
        self.V_App = np.array(addbinvars(self.n_koma,self.n_emp)) 
        self.df_Shift["V_need_person"] = addvars(self.n_koma)
        self.V_least_Shift = addvars(self.n_emp)
        self.df_Shift["V_need_manager"] = addvars(self.n_koma)
    
    def before_main(self):
        self.mokuteki()
        self.seigyo()
        
    def main(self):
        self.m.solve()
    
    def mokuteki(self):
        #目的関数を作成
        self.m += (self.C_need_person * lpSum(self.df_Shift.V_need_person)
              + self.C_not_hope * lpSum(self.df_Shift.apply(lambda r: lpDot(1-r[self.L_emp],self.V_App[r.name]), 1))
              + self.C_least_Shift * lpSum(self.V_least_Shift)
              + self.C_need_manager * lpSum(self.df_Shift.V_need_manager))
    def seigyo(self):
        for _,r in self.df_Shift.iterrows():
            self.m += r.V_need_person >= (lpSum(self.V_App[r.name]) - r.必要人数)
            self.m += r.V_need_person >= -(lpSum(self.V_App[r.name]) - r.必要人数)
            self.m += lpSum(self.V_App[r.name,self.L_manager]) + r.V_need_manager >= 1

        #希望の半分以上
        for j,n in enumerate((self.df_Shift.iloc[:,self.L_emp].sum(0)+1)//2):
            self.m += lpSum(self.V_App[:,j]) + self.V_least_Shift[j] >= n
    
    def result_Shift(self):
        result = np.vectorize(value)(self.V_App).astype(int)
        result = result.T
        df_result = pd.DataFrame(data=result)
        df_result = df_result.replace(1,"○")
        self.cost = value(self.m.objective)
        return df_result
