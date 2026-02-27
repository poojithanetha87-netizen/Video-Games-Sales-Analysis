import pandas as pd

Games=pd.read_csv("games.csv")

print(Games)

print(Games.dtypes)

#changing the datatype of Release Date,rating, Plays, Playing, Backlogs, Wishlist.

Games["Release_Date"]=pd.to_datetime(Games["Release_Date"],format='%b %d, %Y',errors='coerce').fillna(method='ffill') 

Games['Rating']=Games['Rating'].astype(float)

#changing the numeric values which are present in ex:2.5k to 2500 for further analysis comfortness 
def convert_intoN(n):
     if isinstance(n,object) and n.endswith('K'): 
        x=n.rstrip('K') 
        y=float(x)*1000 
        return y 
     else: return n 

lst_of_cl=['Number_of_Reviews','Times_Listed','Plays','Playing','Backlogs','Wishlist']

for col in lst_of_cl:
     
 Games[col]=Games[col].apply(convert_intoN)

 Games[col]=Games[col].astype(int)


print(Games.dtypes)

import psycopg2

conn=None
cur=None
try:
    conn=psycopg2.connect(
        host='localhost',
        database='Video_Games_project',
        user='postgres',
        password='Poojitha@123',
        port=5432)
    cur=conn.cursor()

    Create_table='''Create table if not exists Games_Ds(
      game_n SERIAL PRIMARY KEY,
      Title	Varchar(200),
      Release_Date timestamp,
      Team	Text,
      Rating float,
      Times_Listed	int,
      Number_of_Reviews	int,
      Genres	Text,
      Summary	Text,
      Reviews	Text,
      Plays	int,
      Playing	int,
      Backlogs	int,
      Wishlist int);

     '''
    cur.execute(Create_table)
    conn.commit()
    print("Table created")

    insert_query='''insert into Games_Ds(Title,Release_Date,
    Team,Rating ,Times_Listed,Number_of_Reviews,Genres,Summary,Reviews,Plays,Playing,Backlogs,
      Wishlist) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''

    data_to_insert=[(
       row['Title'],row['Release_Date'],
    row['Team'],row['Rating'] ,row['Times_Listed'],row['Number_of_Reviews'],row['Genres'],row['Summary'],row['Reviews'],row['Plays'],row['Playing'],row['Backlogs'],
     row['Wishlist']) 
     
    for _,row in Games.iterrows()
    
    ]
    cur.executemany(insert_query,data_to_insert)
    conn.commit()

except Exception as error:
   print(error)
finally:
 if cur is not None:
    cur.close()
 if conn is not None:    
    conn.close()




