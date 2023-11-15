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

    
    def clean_df(self):
        """
        This function cleans the dataframe

        Args:
            df (pd.DataFrame): dataframe to be cleaned

        Returns:
            pd.DataFrame: cleaned dataframe
        """

        df = self.df

        # Extracting successfull and failed projects from status column
        if df["state"].nunique() > 2: 
            values = ['live', 'started', 'submitted','canceled']
            #extract rows with only successful or failed
            df = df[df.state.isin(values) == False]
        
        # Extracting the necessary columns
        desired_columns = ['name','category','launched_at','deadline','backers_count','pledged','converted_pledged_amount','goal','country','country_displayable_name','state']
        df = df[desired_columns]
        df = df.drop_duplicates()

        # Convert category column to json
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

        # Convert launched_at and deadline columns to datetime
        df["launched_at"] = df["launched_at"].apply(datetime_converter)
        df["deadline"] = df["deadline"].apply(datetime_converter)

        # Extracting the days from launched_at and deadline columns
        df["days"] = pd.to_datetime(df["deadline"]) - pd.to_datetime(df["launched_at"])
        df["days"] = df["days"].astype(str)
        df["days"] = df["days"].apply(day_extractor)

        # Since None is also a value in sub_category column, replacing Null/NaN values with "None"
        df["sub_category"].fillna("None",inplace=True)

        # Arranging the necessary columns in proper order
        cleaned_df = df[['name', 'parent_category', 'sub_category','days','backers_count', 'pledged','converted_pledged_amount', 'goal','country', 'country_displayable_name', 'state']]
        
        return cleaned_df


class SQL:
    """
    This class is used to creat a database and table in MySQL and insert the values into the table

    Args:
        host (str): host name
        user (str): username
        password (str): password
        database (str): database name
        table (str): table name
    
    Attributes:
        host (str): host name
        user (str): username
        password (str): password
        database (str): database name
        table (str): table name
        port (int): port number
        engine (sqlalchemy.engine.base.Engine): engine object

    Methods:
        create_db: creates a database
        create_table: creates a table
        insert_values: inserts values into the table
        insert_all: inserts all the values from csv files into the table
        table_to_df: converts the table into a dataframe
        df_to_table: converts the dataframe into a table
    """


    def __init__(self, host: str, user: str, password: str, database: str, table: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.port = 3306
        self.engine = create_engine(
                url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                    self.user, self.password, self.host, self.port, self.database
                ))
    

    def create_db(self):
        try:
            conn = sql.connect(host=self.host, user=self.user,
                                password=self.password)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE {}".format(self.database))
                print("{} database created".format(self.database))
                conn.close()
        except Error as e:
            print("Error while connecting to Mysql", e)


    def create_table(self):
        try:
            conn = sql.connect(host=self.host, user=self.user,
                                    password=self.password, database=self.database)
            if conn.is_connected():
                cursor = conn.cursor() 
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ",record)
                cursor.execute('DROP TABLE IF EXISTS {};'.format(self.table))
                print('Creating table.....')
                cursor.execute('CREATE TABLE {}(name CHAR(100) NOT NULL, parent_category CHAR(30) NOT NULL, sub_category CHAR(30) NOT NULL, days INTEGER NOT NULL, backers_count INTEGER NOT NULL, pledged_amt DECIMAL(10, 2) NOT NULL, converted_pledged_amt DECIMAL(10, 2) NOT NULL, goal INTEGER NOT NULL, country CHAR(10) NOT NULL, country_disp_name CHAR(30) NOT NULL, state CHAR(20) NOT NULL )'.format(self.table))
                print("{} table is created.....".format(self.table))
                conn.close()
        except Error as e:
            print("Error while connecting to Mysql", e)


    def insert_values(self, df: pd.DataFrame):
        """
        This function inserts the values into the table from the dataframe
        """
        try:
            conn = sql.connect(host=self.host,
                            database=self.database,
                            user=self.user,
                            password=self.password)
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ",record)
                print("Inserting Values into table")
                for i, row in df.iterrows():
                    query = "INSERT INTO {}.{} VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(self.database, self.table)
                    cursor.execute(query, tuple(row))
                    print("Record inserted")
                    conn.commit()
                print("Inserting completed")
                conn.close()    
        except Error as e:
            print("Error while connecting to MYSQL",e)


    def insert_all(self):
        file_path = "../data/csv_files/Kickstarter.csv"
        data = CleanDF(file_path)
        cleaned_df = data.clean_df()
        self.insert_values(cleaned_df)

        for i in range(1,66):
            path = "../data/csv_files/"
            i = str(i)
            if len(i) == 1:
                file_name = "Kickstarter00" + i + ".csv"
                path = path + file_name
                df = CleanDF(path)
                cleaned_df = df.clean_df()
                self.insert_values(cleaned_df)
            else:
                file_name = "Kickstarter0" + i + ".csv"
                path = path + file_name
                df = CleanDF(path)
                cleaned_df = df.clean_df()
                self.insert_values(cleaned_df)


    def table_to_df(self):
        try:
            print("Connected to the {}".format(self.database))
            df = pd.read_sql_table(self.table, self.engine)
            
            return df
        except Exception as e:
            print("Error in connecting to the database", e)

    
    def df_to_table(self, df: pd.DataFrame, table_name: str):
        """
        This function converts the dataframe into a table

        Args:
            df (pd.DataFrame): dataframe to be converted into a table
            table_name (str): name of the table

        Returns:
            table: A table is created in the database
        """

        return df.to_sql(table_name, con=self.engine, index=False, if_exists='replace')





