import pyodbc
from pyodbc import Error
import pandas as pd

def connect_game():
    try:
        con = pyodbc.connect("DRIVER={SQL Server};SERVER=DESKTOP-SH243I1\LETHIKIMLE;DATABASE=Game_Database;Trusted_Connection=yes;")
        return con

    except Error:
        print(Error)

def connect_user():
    try:
        con = pyodbc.connect("DRIVER={SQL Server};SERVER=DESKTOP-SH243I1\LETHIKIMLE;DATABASE=User_Database;Trusted_Connection=yes;")
        return con

    except Error:
        print(Error)

def sql_exec(con, command):

    cursorObj = con.cursor()
    cursorObj.execute(command)
    con.commit()












