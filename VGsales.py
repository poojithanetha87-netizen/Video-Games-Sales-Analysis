import pandas as pd 
import numpy as np


VGS=pd.read_csv("vgsales.csv")
#understanding the data set
print(VGS.head())

print(VGS.dtypes)

print(VGS.isna().sum())

Games_Name=VGS.loc[VGS['Year_P'].isna(),'NameG']
print(Games_Name)

Dul_count=VGS.apply(lambda col:col.duplicated().sum())

print(Dul_count)




VGS_Kaggle=pd.read_csv('Video_Game_Sales_as_of_Jan_2017.csv')
'''In VGS data we have "Unknown" as Publisher name changing
 that as NAN to get updated those fields by upcoming steps'''

VGS['Publisher']=VGS['Publisher'].replace('Unknown',np.nan)


#Updating NAN values in publisher column
merge = VGS.merge(
    VGS_Kaggle[['Name_','Platform','Genre','Publisher_','Global_Sales']],
    left_on=['NameG','Platform','Genre','Global_Sales'],
    right_on=['Name_','Platform','Genre','Global_Sales'],
    how='left'
)

VGS['Publisher'] = VGS['Publisher'].combine_first(merge['Publisher_'])


print(VGS.isna().sum())
#updating NAN values in year_P based on 5 matching columns

Merge2=VGS.merge(VGS_Kaggle[['Name_','Platform','Year_of_Release','Genre','Publisher_','Global_Sales']],
        left_on=['NameG','Platform','Genre','Publisher','Global_Sales'],
        right_on=['Name_','Platform','Genre','Publisher_','Global_Sales'],
        how='left')                                 
VGS['Year_P']=VGS['Year_P'].combine_first(Merge2['Year_of_Release'])
print(VGS.isna().sum())
#updating NAN values in year_P based on 4 matching columns
Merge3=VGS.merge(VGS_Kaggle[['Name_','Platform','Year_of_Release','Genre','Publisher_','Global_Sales']],
        left_on=['NameG','Platform','Genre','Publisher'],
        right_on=['Name_','Platform','Genre','Publisher_'],
        how='left')                                 
VGS['Year_P']=VGS['Year_P'].combine_first(Merge3['Year_of_Release'])
print(VGS.isna().sum())

#7 Publisher fields are NAN we will eliminate Gobalsales matching condition and we will try to update those
merge1 = VGS.merge(
    VGS_Kaggle[['Name_','Platform','Genre','Publisher_','Global_Sales']],
    left_on=['NameG','Platform','Genre'],
    right_on=['Name_','Platform','Genre'],
    how='left'
)

VGS['Publisher'] = VGS['Publisher'].combine_first(merge1['Publisher_'])

print(VGS.isna().sum())

#updating median of year in remaning NAN fields 


VGS=VGS.dropna(subset=['Publisher'])
print(VGS)
VGS['Year_P']=VGS['Year_P'].fillna(VGS['Year_P'].median())




print(VGS.isna().sum())

VGS['Year_P']=VGS['Year_P'].astype(int)
print(VGS.dtypes)


import psycopg2

conn=None
cur=None

try:
    conn=psycopg2.connect(host='localhost',
        database='Video_Games_project',
        user='postgres',
        password='Poojitha@123',
        port=5432)
    cur=conn.cursor()
    cur.execute('DROP TABLE IF EXISTS VGS;')

    Create_table='''Create table VGS(
        Ranks_	int,
        NameG	Text,
        Platform Text,
        Year_P int,
        Genre varchar(100),
    	Publisher Varchar(200),
    	NA_Sales float,
    	EU_Sales float,
        JP_Sales float,
    	Other_Sales float,
    	Global_Sales float);'''
    cur.execute(Create_table)
    conn.commit()

    insert=''' Insert into VGS(Ranks_ ,NameG,Platform,Year_P,Genre,
	Publisher,	NA_Sales,	EU_Sales,	JP_Sales,	Other_Sales,	Global_Sales) 
    Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    Values=[(
    row['Ranks_'],
    row['NameG'],
    row['Platform'],
    row['Year_P'],
    row['Genre'],
    row['Publisher'],
    row['NA_Sales'],
    row['EU_Sales'],
    row['JP_Sales'],
    row['Other_Sales'],
    row['Global_Sales']
    )
    for _,row in VGS.iterrows()]

    cur.executemany(insert,Values)
    conn.commit()

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()        