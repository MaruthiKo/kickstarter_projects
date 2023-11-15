# Import required libraries
import mysql.connector as sql
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
import json 
from helper_functions import datetime_converter, day_extractor
from pathlib import Path


class CleanDF:
    """
    This class cleans the dataframe

    Args:
        path (str): path to the csv file

    Attributes:
        df (pd.DataFrame): dataframe to be cleaned
    
    Methods:
        clean_df: cleans the dataframe
    """


    def __init__(self, path: str):
        self.df = pd.read_csv(path)

    
    def clean_df(self, df: pd.DataFrame):
        """
        This function cleans the dataframe

        Args:
            df (pd.DataFrame): dataframe to be cleaned

        Returns:
            pd.DataFrame: cleaned dataframe
        """
        df = self.df

        if df["state"].nunique() > 2:
            #define values
            values = ['live', 'started', 'submitted','canceled']
            #extract rows with only successful or failed
            df = df[df.state.isin(values) == False]
        desired_columns = ['name','category','launched_at','deadline','backers_count','pledged','converted_pledged_amount','goal','country','country_displayable_name','state']
        df = df[desired_columns]
        df = df.drop_duplicates()
        df["category"] = [json.loads(cat) for cat in df.category.values]
        parent_category = [] 
        for cat in df["category"]:
            if "parent_name" in cat.keys():
                parent_category.append(cat["parent_name"])
            else:
                parent_category.append(cat["name"])
        df["parent_category"] = parent_category
        sub_category = []
        for cat in df["category"]:
            if 'parent_name' not in cat.keys():
                sub_category.append(None)
            else:
                sub_category.append(cat["name"])
        df["sub_category"] = sub_category
        df = df.drop(columns="category", axis=1)
        df["launched_at"] = df["launched_at"].apply(datetime_converter)
        df["deadline"] = df["deadline"].apply(datetime_converter)
        df["days"] = pd.to_datetime(df["deadline"]) - pd.to_datetime(df["launched_at"])
        df["days"] = df["days"].astype(str)
        df["days"] = df["days"].apply(day_extractor)
        df["sub_category"].fillna("None",inplace=True)
        # Arranging the necessary columns in proper order
        cleaned_df = df[['name', 'parent_category', 'sub_category','days','backers_count', 'pledged','converted_pledged_amount', 'goal','country', 'country_displayable_name', 'state']]
        
        return cleaned_df

# connect to sql

def create_db(host: str, user: str, password: str, database: str):
    try:
        conn = sql.connect(host=host, user=user,
                            password=password)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE {}".format(database))
            print("{} database created".format(database))
            conn.close()
    except Error as e:
        print("Error while connecting to Mysql", e)

def create_table(host: str, user: str, password: str, database: str, table: str):
    try:
        conn = sql.connect(host=host, user=user,
                                password=password, database=database)
        if conn.is_connected():
            cursor = conn.cursor() 
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ",record)
            cursor.execute('DROP TABLE IF EXISTS {};'.format(table))
            print('Creating table.....')
            cursor.execute('CREATE TABLE {}(name CHAR(100) NOT NULL, parent_category CHAR(30) NOT NULL, sub_category CHAR(30) NOT NULL, days INTEGER NOT NULL, backers_count INTEGER NOT NULL, pledged_amt DECIMAL(10, 2) NOT NULL, converted_pledged_amt DECIMAL(10, 2) NOT NULL, goal INTEGER NOT NULL, country CHAR(10) NOT NULL, country_disp_name CHAR(30) NOT NULL, state CHAR(20) NOT NULL )'.format(table))
            print("{} table is created.....".format(table))
            conn.close()
    except Error as e:
        print("Error while connecting to Mysql", e)

def insert_values(host: str, database: str, user: str, password: str, table: str, df: pd.DataFrame):
    try:
        conn = sql.connect(host=host,
                            database=database,
                            user=user,
                            password=password)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ",record)
            print("Inserting Values into table")
            for i, row in df.iterrows():
                query = "INSERT INTO {}.{} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(database, table)
                cursor.execute(query, tuple(row))
                print("Record inserted")
                conn.commit()
            print("Inserting completed")
            conn.close()    
    except Error as e:
        print("Error while connecting to MYSQL",e)

def insert_all():
    file_path = "../data/csv_files/Kickstarter.csv"
    data = pd.read_csv(file_path)
    cleaned_df = clean_df(data)
    insert_values(cleaned_df)

    for i in range(1,66):
        path = "../data/csv_files/"
        i = str(i)
        if len(i) == 1:
            file_name = "Kickstarter00" + i + ".csv"
            path = path + file_name
            df = pd.read_csv(path)
            cleaned_df = clean_df(df)
            insert_values(cleaned_df)
        else:
            file_name = "Kickstarter0" + i + ".csv"
            path = path + file_name
            df = pd.read_csv(path)
            cleaned_df = clean_df(df)
            insert_values(cleaned_df)

def table_to_df(host: str, user: str, password: str, database: str, table: str):
    try:
        port = 3306
        engine = create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            ))
        print("Connected to the {}".format(database))
        df = pd.read_sql_table(table,engine)
        
        return df
    except Exception as ex:
        print("Error in connecting to the database", ex)


def df_to_sql(df: pd.DataFrame,table_name: str,engine):
    return df.to_sql(table_name, con=engine, index=False, if_exists='replace')

def df_to_csv(df: pd.DataFrame, file_path: str):
    return df.to_csv(file_path, index=False)
