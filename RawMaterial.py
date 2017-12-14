import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from matplotlib import style
style.use('ggplot')

f = open('C:\\Users\\童安弘\\Desktop\\資料夾們\\財報狗\\原物料相關性分析\\LME_現貨_銅.csv')
f2 = open('C:\\Users\\童安弘\\Desktop\\資料夾們\\財報狗\\原物料相關性分析\\歷史股價.csv')

d = pd.read_csv(f)
df = pd.DataFrame(d)
d2= pd.read_csv(f2)
df2 = pd.DataFrame(d2)
df.columns=['date','price']
df = df.drop([0,1,2]).merge(df2, on='date', how='left').sort_values(['ticker','date']).dropna()
du= df.drop_duplicates(['ticker'],keep='first',inplace=False).ticker

stkname = []
for x in du:
    x = str(x)
    stkname.append(x)
print('Stock number：', stkname)
highcorrelation = []
a = 0
while a < len(stkname):
    stknum = float(stkname[a])
    df_corr = df[df.ticker == stknum]
    df_corr = df_corr.drop('date',1).drop('ticker',1).dropna()
    df_price = np.array(df_corr.drop('closing',1))
    df_closing = np.array(df_corr.drop('price',1))
    lm = LinearRegression()  
    lm.fit(np.reshape(df_price, (len(df_price), 1)), np.reshape(df_closing, (len(df_closing), 1)))
    if lm.coef_ >= 0.7:
        print('高相關: 股票代號',stknum,'係數: ',lm.coef_)  
    if lm.coef_ > 0.5 and lm.coef_ < 0.7 :
        df2_price = pd.DataFrame(df_price)[30:]
        df2_closing = pd.DataFrame(df_closing)[:-30]
        lm2 = LinearRegression()
        lm2.fit(np.reshape(df2_price, (len(df2_price), 1)), np.reshape(df2_closing, (len(df2_closing), 1)))
        if lm2.coef_ > 0.7:
            print('高相關: 股票代號',stknum,'係數: ',lm2.coef_,'遞延一個月')
        else:
            df3_price = pd.DataFrame(df_price)[60:]
            df3_closing = pd.DataFrame(df_closing)[:-60]
            lm3 = LinearRegression()
            lm3.fit(np.reshape(df3_price, (len(df3_price), 1)), np.reshape(df3_closing, (len(df3_closing), 1)))
            if lm3.coef_ > 0.7:
                print('高相關: 股票代號',stknum,'係數: ',lm3.coef_,'遞延二個月')
            else :
                print('中相關: 股票代號',stknum,'係數: ',lm.coef_)
    else :
        print('低相關: 股票代號',stknum,'係數: ',lm.coef_)  
    a+=1

f.close()
f2.close()