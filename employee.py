#第五回　関数化
#ここから
import pandas as pd
import numpy as np
from random import random


file_name = "shift.xlsm"

def read_excel(file_name):
    df = pd.read_excel(file_name)
    df = df.iloc[4:14,1:33]
    df = df.fillna(0)
    df = df.replace("○",2)

    holiday = df.iloc[:,31:32].reset_index(drop=True)
    holiday.colums = ["休日数"]

    kiso = df.iloc[:,0:31].reset_index(drop=True)
    kiso.columns = [i+1 for i in range(len(kiso.columns))]
    return kiso,holiday

#第一世代
def first_gene(kiso,holiday):
    days = len(kiso.columns)
    kiso_copy = kiso.copy()
    
    for k in range(len(kiso_copy)):
        h = []

        #休日数だけループ
        while len(h) < holiday.loc[k][0]:
            n = np.random.randint(1, days)
            if not n in h:
                h.append(n)
        #休日を埋め込む
        for i in h:
            if kiso_copy.loc[k,i] == 0:
                kiso_copy.loc[k,i] = 1
        
        return kiso_copy
                
def holiday_fix(kiso_copy,holiday):
    days = len(kiso.columns)
    for k in range(len(kiso_copy)):
        if np.count_nonzero(kiso_copy.iloc[k:k+1]) != holiday.loc[k][0]:
            #sはあと何日休日を入れた良いのか。０が山,-は足りない。+は多い
            s = np.count_nonzero(kiso_copy.iloc[k:k+1]) - holiday.loc[k][0]
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

def evaluation_function(kiso_copy):
    #四回目
    #希望休を1に変換
    eva = kiso_copy.replace(2,1)

    #評価項目
    """
    0が働く
    １が休み
    """
    score = 0

    for k in range(len(eva)):
        #文字列として結合
        x = "".join([str(i) for i in np.array(eva.iloc[k:k+1]).flatten()])
        #五連勤以上の評価　三連休より高い値になる
        score += np.sum([((2 - len(i))**2)* -1 for i in x.split("1") if len(i) >= 5])

        #三連休以上の評価
        score += np.sum([((1 - len(i))**2) *-1 for i in x.split("0") if len(i) >= 3])

        #飛び石連休の評価
        score += -10*(len(x.split("101"))-1)

        #出勤数の評価(縦軸)
        #全体の七割が良いとしているため,全体の七割から働いている人をひいている。
        score += np.sum([abs(len(eva)*0.7 - (len(eva) - np.sum(eva[k]))) * -4 for k in eva.columns])
    return score

#一様交叉
"""
ep:一様交叉の確率（例５０%,0.5）
sd:突然変異の確率（例５%,0.05）
p1:個体１
p2:個体２
"""
def crossover(ep,sd,p1,p2):
    #一ヶ月の日数
    days = len(p1.columns)
    
    #一次元化
    p1 = np.array(p1).flatten()
    p2 = np.array(p2).flatten()
    
    #子の変数
    ch1 = []
    ch2 = []
    
    for p1_,p2_ in zip(p1,p2):
        x = True if ep > random() else False
        
        if x == True:
            ch1.append(p1_)
            ch2.append(p2_)
        else:
            ch1.append(p2_)
            ch2.append(p1_)
    
    #突然変異
    ch1,ch2 = mutation( sd, np.array(ch1).flatten(), np.array(ch2).flatten())
    
    #pandasに変換
    ch1 = pd.DataFrame(ch1.reshape(int(len(ch1)/days),days))
    ch2 = pd.DataFrame(ch2.reshape(int(len(ch2)/days),days))
    
    #列名変換
    ch1.columns = [i+1 for i in range(len(ch1.columns))]
    ch2.columns = [i+1 for i in range(len(ch2.columns))]
    
    return ch1,ch2
    
def mutation(sd,ch1,ch2):
    
    x = True if sd > random() else False
    
    if x == True:
        rand = np.random.permutation([i for i in range(len(ch1))])
        rand = rand[:int(len(ch1)//10)]
        
        for i in rand:
            if ch1[i] == 1:
                ch1[i] = 0
            if ch1[i] == 0:
                ch1[i] = 1
    x = True if sd > random() else False
    
    if x == True:
        rand = np.random.permutation([i for i in range(len(ch2))])
        rand = rand[:int(len(ch1)//10)]
        
        for i in rand:
            if ch2[i] == 1:
                ch2[i] = 0
            if ch2[i] == 0:
                ch2[i] = 1
    return ch1,ch2

#遺伝的アルゴリズム第七回
kiso,holiday = read_excel(file_name)
parent = []
#親の保存
for i in range(100):
    #第一世代
    kiso_copy = first_gene(kiso,holiday)
    
    #休日数の修正
    kiso_copy = holiday_fix(kiso_copy, holiday)
    
    #評価
    score = evaluation_function(kiso_copy)
    
    #第一世代を格納
    parent.append([score,kiso_copy])
    
#上位交換
elite_length = 20
#世代数
gene_length = 50

#一様交叉確率
ep = 0.5
#突然変異確率
sd = 0.05

for i in range(gene_length):
    #点数で並び替え
    parent = sorted(np.array(parent), key=lambda x: -x[0])
    
    #上位個体を選別
    parent = parent[:elite_length]
    
    #最高得点の更新
    if i == 0 or top[0] < parent[0][0]:
        top = parent[0]
    else:
        parent.append(top)
    
    #各世代
    print("第"+str(i+1)+"世代")
    #各世代の最高得点
    print(top[0])
    print(np.array(top[1]))
    
    #子世代
    children = []
    
    #遺伝子操作
    for k1,v1 in enumerate(parent):
        for k2,v2 in enumerate(parent):
            if k1 < k2:
                #一様交叉
                ch1,ch2 = crossover(ep,sd,v1[1],v2[1])
                #休日数変更
                ch1 = holiday_fix(ch1,holiday)
                ch2 = holiday_fix(ch2,holiday)
                #評価
                score1 = evaluation_function(ch1)
                score2 = evaluation_function(ch2)
                
                #子孫を格納
                children.append([score1,ch1])
                children.append([score2,ch2])
                
    #子を親にコピー
    parent = children.copy()
    
x = top[1].replace(1,"○").replace(2,"◎").replace(0,"")
x.to_excel("shift.xlsx")