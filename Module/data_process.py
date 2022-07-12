from unicodedata import name
import Module.data_layer as dtl
import pandas as pd
from datetime import date
from calendar import monthrange
pd.set_option('mode.chained_assignment', None)

class Game_Data():

    def __init__(self):
        self.conn= dtl.connect_game()

    def get_question(self):
        df = pd.read_sql_query('SELECT * FROM QUESTION', self.conn)
        df.to_csv('Question.csv', index=False)
        return df
        
    def get_answer(self):
        df = pd.read_sql_query('SELECT * FROM ANSWER', self.conn)
        df.to_csv('Answer.csv', index=False)
        return df

    def get_multichoices(self):
        df = pd.read_sql_query('SELECT * FROM MULTICHOICES', self.conn)
        df.to_csv('Multichoices.csv', index=False)
        return df

    def game_data(self):
        file1=self.get_question()
        file2=self.get_answer()
        file3=self.get_multichoices()
        return ['Question.csv','Answer.csv', 'Multichoices.csv']

class User_Data():

    def __init__(self):
        self.conn=dtl.connect_user()
        self.df1 = pd.read_sql_query('SELECT * FROM User_Infor', self.conn)
        self.df2= pd.read_sql_query('SELECT * FROM User_Play', self.conn)
        self.df3= pd.read_sql_query('SELECT * FROM User_Data', self.conn)

    def get_user_whole(self):
        ''' Get number of signed in users, No of User each day, lastest user, online_user'''
        
        total_count=len(self.df1.index)
        today = date.today()
        
        cartier = self.df1.groupby(['DateSignIn'])['UserID'].count().to_frame()
        cartier.columns=['No_Users']
        cartier.reset_index(level = [0], inplace=True)

        lastest_no_user=0
        for i in range(len(cartier.index)):
            if str(cartier.DateSignIn[i]) == str(today):
                lastest_no_user=int(cartier.No_Users[i])
                break
        return(total_count, lastest_no_user, cartier)
        

    def get_rank_score(self, signal, time_span=None):
        if (signal=='all'):
            sort=self.df2.sort_values(by=['Highest_Score'], ascending=False, inplace=False)
            save_iden=sort.iloc[:,[True, False, True]]
            rank_list=pd.merge(save_iden,self.df1, how='inner')
            final=rank_list.drop(['UserID','Password', 'DateSignIn'],  axis = 1, inplace=False)
            final=final[['Username', 'Highest_Score']]
            return final
        else:
            select = pd.read_sql_query("SELECT * FROM User_Data WHERE Date BETWEEN '{:s}' AND '{:s}'".format(time_span[0], time_span[1]), self.conn)
            select['Score']=select['Score'].astype(int)
            group=select.groupby(['UserID'])['Score'].max().to_frame()
            sort=group.sort_values(by=['Score'], ascending=False, inplace=False)
            sort.reset_index(level = [0], inplace=True)
            rank_list=pd.merge(sort,self.df1, how='inner')
            final=rank_list.drop(['UserID','Password','DateSignIn'],  axis = 1, inplace=False)
            final=final[['Username', 'Score']]
            return final


    def get_rank_time(self, signal, time_span=None):
        if (signal=='all'):
            sort=self.df2.sort_values(by=['Play_Time'], ascending=False, inplace=False)
            save_iden=sort.iloc[:,[True, True, False]]
            rank_list=pd.merge(save_iden,self.df1, how='inner')
            final=rank_list.drop(['UserID','Password', 'DateSignIn'],  axis = 1, inplace=False)
            final=final[['Username', 'Play_Time']]
            return final
        
        else:
            select = pd.read_sql_query("SELECT * FROM User_Data WHERE Date BETWEEN '{:s}' AND '{:s}'".format(time_span[0], time_span[1]), self.conn)
            group=select.groupby(['UserID'])['ID'].count().to_frame()
            group.columns=['PlayTime']
            sort=group.sort_values(by=['PlayTime'], ascending=False, inplace=False)
            sort.reset_index(level = [0], inplace=True)
            rank_list=pd.merge(sort,self.df1, how='inner')
            final=rank_list.drop(['UserID','Password','DateSignIn'],  axis = 1, inplace=False)
            final=final[['Username', 'PlayTime']]
            return final


    def check_user(self, infor):
        infor=infor.split(',')
        if len(infor)==2:
            name=infor[0]
            password=infor[1]
            for i in range(0, len(self.df1.index)):
                if str(self.df1.Username[i]).strip()==name and str(self.df1.Password[i]).strip()==password:
                    return self.df1.UserID[i]
        return 'None'

    def add_user(self, infor):

        def get_nextID(prevID):

            format1=lambda x: '00'+str(x)
            format2=lambda x: '0'+str(x)
            print(prevID+"jj")
            num=int(prevID[-3:])+1
            if num<10:
                num=format1(num)
            elif num<100:
                num=format2(num)
            else:
                num=str(num)
            next='SD'+str(num)
            return next

        infor=infor.split(',')
        if len(infor)==2:
            name=infor[0]
            password=infor[1]
            res_day=str(date.today())

            for i in range(0, len(self.df1.index)):
                if str(self.df1.Username[i]).strip()==name:
                    return 'None'

            lastID=str(self.df1.UserID[len(self.df1.index)-1]).strip()
            nextID=get_nextID(lastID)

            command="INSERT INTO User_Infor VALUES ('{:s}', '{:s}', '{:s}', '{:s}')".format(nextID, name, password, res_day)
            dtl.sql_exec(self.conn,command)
            self.reload()
            return nextID
        return 'None'

    def update_user_dataplay(self, infor):

        infor=infor.split(',')
        if len(infor)==3:
            userID=infor[0]
            Score=int(infor[1])
            date_play=infor[2]
            number=len(self.df3.index)
            command="INSERT INTO User_Data VALUES ('{:d}', '{:s}', '{:d}', '{:s}')".format(number, userID, Score, date_play)
            dtl.sql_exec(self.conn,command)
            self.reload()
            print(userID)
            for item in range(len(self.df2.index)):
                user=self.df2.iloc[item].to_list()
                print(user)
                if user[0].strip()==userID.strip():
                    playtime=user[1]+1
                    if user[2]<Score:
                        command_update="UPDATE User_Play SET Highest_Score={:d} WHERE UserID like '{:s}%'".format(Score, userID)
                        dtl.sql_exec(self.conn, command_update)

                    command_update="UPDATE User_Play SET Play_Time={:d} WHERE UserID like '{:s}%'".format(playtime, userID)
                    dtl.sql_exec(self.conn, command_update)
                    self.reload()
                    return 'True'

            command="INSERT INTO User_Play VALUES ('{:s}', {:d}, {:d})".format(userID, 1, Score)
            dtl.sql_exec(self.conn,command)
            self.reload()
            return 'True'
        return 'None'
        
    def reload(self):
        self.df1 = pd.read_sql_query('SELECT * FROM User_Infor', self.conn)
        self.df2= pd.read_sql_query('SELECT * FROM User_Play', self.conn)
        self.df3= pd.read_sql_query('SELECT * FROM User_Data', self.conn)


    def get_statistics(self, request, infor=None):
        
        a=self.df1['DateSignIn'].str.split("-",expand=True)
        temp=pd.concat([self.df1, a],axis=1)
        temp = temp.set_axis(['id', 'UserName', 'PassWord', 'DateSignIn', 'Year','Month','Day'], axis=1, inplace=False)
        temp=temp[['id', 'UserName', 'PassWord', 'DateSignIn', 'Day','Month','Year']]

        def get_min_max(dict):
            lst_val = list(dict.values())
            lst_ke = list(dict.keys())
            return (lst_ke[lst_val.index(max(lst_val))], max(lst_val)), (lst_ke[lst_val.index(min(lst_val))], min(lst_val))

        def get_statistic_year(df):
            f_year=df.groupby('Year')['id'].count()
            return f_year.to_dict()

        def get_statistic_month(year, df):

            df= df[df['DateSignIn'].str.contains(year)]
            df=df.sort_values(by=['Month'], inplace=False)
            df=df.groupby('Month')['id'].count()
            df.index=df.index.astype(int)
            dict_month=df.to_dict()
            for i in range(1, 13):
                if i not in dict_month.keys():
                    dict_month[i]=0

            max_item, min_item=get_min_max(dict_month)
            return (dict_month, max_item, min_item)

        def get_statistic_quarter(year, df):
            
            df= df[df['DateSignIn'].str.contains(year)]
            df['Month']=df['Month'].astype(int)
            df['Quarter']=(df['Month']-1)//3+1
            df=df.groupby('Quarter')['id'].count()
            df=df.to_dict()
            for i in range(1, 5):
                if i not in df.keys():
                    df[i]=0
            max_item, min_item=get_min_max(df)
            return (df, max_item, min_item)

        def get_statistic_date(month,year,df):

            df= df[df['Year'].str.contains(year)]
            df= df[df['Month'].str.contains(month)]
            df=df.groupby('Day')['id'].count()
            df.index=df.index.astype(int)
            df=df.to_dict()
            year=int(year)
            month=int(month)
            num_days = monthrange(year, month)[1]
            for i in range(1, num_days+1):
                if i not in df.keys():
                    df[i]=0
            max_item, min_item=get_min_max(df)
            return (df, max_item, min_item)

        def get_statistic_mquarter(quarter,year,df):

            df= df[df['Year'].str.contains(year)]
            df['Month']=df['Month'].astype(int)
            df['Quarter']=(df['Month']-1)//3+1
            df['Quarter']=df['Quarter'].astype(str)
            df= df[df['Quarter'].str.contains(quarter)]
            df=df.groupby('Month')['id'].count()
            df.index=df.index.astype(int)
            df=df.to_dict()
            year=int(year)
            quarter=int(quarter)
            start=(quarter-1)*3+1
            end=start+3
            for i in range(start, end):
                if i not in df.keys():
                    df[i]=0
            max_item, min_item=get_min_max(df)
            return (df, max_item, min_item)

        if request==0:
            return(get_statistic_year(temp))
        elif request==1:
            return(get_statistic_month(infor, temp))
        elif request==2:
            return(get_statistic_quarter(infor, temp))
        elif request==3:
            return(get_statistic_date(infor[0], infor[1], temp))
        else:
            return(get_statistic_mquarter(infor[0], infor[1], temp))


# user.get_statistics(2,'2019')
# user.get_statistics(4, ['4', '2019'])





