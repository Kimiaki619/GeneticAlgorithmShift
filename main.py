import read_excel
import New_Shift

import pandas as pd
import openpyxl

"""
ここのpythonファイルでエクセルファイルを読み込んだのちに組合せ最適化をして、Book2.xlsxのファイルに出力値を入れている。
Book2.xlsxはプログラムを実行するたびに新しいファイルになる。
Shift_excel:シフトの希望日を入れたエクセルファイル
Shift_name:シフトの希望日を入れたエクセルファイルのシート
emp_num：従業員の人数
work_day：勤務日の日数
"""

#エクセルファイルを読み込む
df_read = read_excel.Shift_read(Shift_excel="Book1.xlsm", Shift_name="Sheet1", emp_num=10, work_day= 30)
df_Shift = df_read.df_Shift
manager = df_read.manager()

#組合せ最適化
Shift = New_Shift.new_Shift(df_Shift,manager)
Shift.before_main()
Shift.main()
df_result = Shift.result_Shift()
print(Shift.cost)

#新しいファイルの名前
path = 'Book2.xlsx'
with pd.ExcelWriter(path) as writer:
    df_result.to_excel(writer, sheet_name='New_Shift')


