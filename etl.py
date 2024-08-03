
import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def extract(country: str = "United+States") -> dict:
    """ This API extracts data from
    http://universities.hipolabs.com
    """
    API_URL = f"http://universities.hipolabs.com/search?country={country}"
    try:
	    response = requests.get(API_URL)
	    response.raise_for_status()
	    data = response.json()
	    return data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def transform(data:dict) -> pd.DataFrame:
    """ Transforms the dataset into desired structure and filters"""
    df = pd.DataFrame(data)
    print(f"Total Number of universities from API {len(data)}")
    
    df = df[df["name"].str.contains("California")]
    print(f"Number of universities in california {len(df)}")
    
    df['domains'] = [','.join(map(str, l)) for l in df['domains']]
    df['web_pages'] = [','.join(map(str, l)) for l in df['web_pages']]
    df = df.reset_index(drop=True)
    return df[["domains","country","web_pages","name"]]

def load(df:pd.DataFrame, table_name:str)-> None:
    # Load environment variables
    load_dotenv()
    
    # MySQL connection parameters
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    host = os.getenv('MYSQL_HOST')
    port = os.getenv('MYSQL_PORT')

    # Create a MySQL engine
    db_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/my_database")
    
    # Load the dataframe into MySQL
    df.to_sql(table_name, db_engine, if_exists='replace', index=False)

if __name__ == "__main__":
	data = extract()
	df = transform(data)
	load(df, table_name='cal_uni')