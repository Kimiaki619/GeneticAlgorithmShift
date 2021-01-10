#シフト表
import pandas as pd
import numpy as np
from random import random

#ファイルを読み込むクラス
class read_EXCEL(object):
	"""cstring for ClassName"""
	def __init__(self, filename="shift.xlsm"):
		self.filename = filename

	def read_excel(self):
		#出勤可能な日と希望出勤数
	    df_read_excel = pd.read_excel(self.file_name)
	    df_read_excel = df_read_excel.iloc[4:14,1:33]
	    df_read_excel = df_read_excel.fillna(0)
	    df_read_excel = df_read_excel.replace("○",1)

	    #希望出勤数
	    work_day = df_read_excel.iloc[:,31:32].reset_index(drop=True)
	    work_day.colums = ["出勤希望"]
	    #出勤可能な日
	    kiso = df_read_excel.iloc[:,0:31].reset_index(drop=True)
	    kiso.columns = [i+1 for i in range(len(kiso.columns))]

	    return kiso,work_day

#遺伝的アルゴリズム
class  Shift_gane(object):
	"""docstring for  """
	def __init__(self, kiso, work_day):
		self.kiso = kiso
		self.work_day = work_day

	def first_gene(self):
	    days = len(self.kiso.columns)
	    kiso_copy = self.kiso.copy()
	    
	    for k in range(len(kiso_copy)):
	        h = []

	        #出勤できる日だけループ
	        while len(h) < self.work_day.loc[k][0]:
	            n = np.random.randint(1, days)
	            if not n in h:
	                h.append(n)
	        #出勤日を埋め込む
	        for i in h:
	            if kiso_copy.loc[k,i] == 1:
	                kiso_copy.loc[k,i] = 2
	        
	        return kiso_copy

	def work_day_fix(self, kiso_copy):
    	days = len(kiso.columns)
	    for k in range(len(kiso_copy)):
	        if np.count_nonzero(kiso_copy.iloc[k:k+1]) != self.work_day.loc[k][0]:
	            #sはあと何日休日を入れた良いのか。０が山,-は足りない。+は多い
	            s = np.count_nonzero(kiso_copy.iloc[k:k+1]) - self.work_day.loc[k][0]
	            buf = 0

	            c1 = 1 if s > 0 else 0
	            c2 = 1 if c1 == 0 else 0
	            while buf < abs(s):
	                n = np.random.randint(1,days)
	                if kiso_copy.loc[k][n] == c1:
	                    buf += 1
	                    #休日を変える
	                    kiso_copy.loc[k,n] = c2
	    return kiso_copy





		