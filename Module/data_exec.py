import Module.data_layer as dtl
import pandas as pd

con= dtl.connect_game()
conUser=dtl.connect_game()

def get_question():
   
    df = pd.read_sql_query('SELECT * FROM QUESTION', con)
    return df
    
def get_answer(QuesID):
    df = pd.read_sql_query("SELECT * FROM ANSWER WHERE QuesID='"+QuesID+"'", con)
    return df.iloc[0][1]
    

def get_multichoices(QuesID):
    df=pd.read_sql_query("SELECT * FROM MULTICHOICES WHERE QuesID='"+QuesID+"'", con)
    return df

