from torch import randint
from data_layer import *
import random
from datetime import *

def randate(start_date):

    end_date = date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date

conn= connect_user()

def Create_data():

    df1 = pd.read_sql_query('SELECT * FROM User_Infor', conn)
    index=0
    for item in range(len(df1.index)):
        user=df1.iloc[item].to_list()
        num=random.randint(5,20)
        for i in range(num):
            num_score=random.randint(100,500)
            rand_date=randate(datetime.strptime(user[-1], '%Y-%m-%d').date())
            str_date= rand_date.strftime('%Y-%m-%d')
            command="INSERT INTO User_Data VALUES ({:d}, '{:s}', '{:d}', '{:s}')".format(index, user[0].strip() ,num_score, str_date)
            sql_exec(conn,command)
            index+=1

Create_data()

df = pd.read_sql_query('SELECT * FROM User_Data', conn)
cartier = df.groupby(['UserID'])['ID'].count().to_frame()
max_score= df.groupby(['UserID'])['Score'].max().to_frame()
cartier['Score']=max_score['Score']
cartier.reset_index(level = [0], inplace=True)

for item in range(len(cartier.index)):
    user=cartier.iloc[item].to_list()
    command="INSERT INTO User_Play VALUES ('{:s}', '{:d}', '{:d}')".format(user[0].strip(),user[1], int(user[2].strip()))
    sql_exec(conn,command)
