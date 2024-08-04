
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sshtunnel import SSHTunnelForwarder

def extract(country: str = "United+States") -> dict:
 
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
  
    df = pd.DataFrame(data)
    print(f"Total Number of universities from API {len(data)}")
    
    df = df[df["name"].str.contains("California")]
    print(f"Number of universities in california {len(df)}")
    
    df['domains'] = [','.join(map(str, i)) for i in df['domains']]
    df['web_pages'] = [','.join(map(str, i)) for i in df['web_pages']]
    df = df.reset_index(drop=True)
    return df[["domains","country","web_pages","name"]]

def load(df:pd.DataFrame, table_name:str)-> None:
    # Load environment variables
    load_dotenv()
    
    # SSH connection parameters
    ssh_host = os.getenv('SSH_HOST')
    ssh_username = os.getenv('SSH_USERNAME')
    ssh_private_key = os.getenv('SSH_PRIVATE_KEY_PATH')


    # MySQL connection parameters
    mysql_user = os.getenv('MYSQL_USER')
    mysql_password = os.getenv('MYSQL_PASSWORD')
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_port = int(os.getenv('MYSQL_PORT'))
    mysql_db = os.getenv('MYSQL_DATABASE')

    with SSHTunnelForwarder(
        (ssh_host, 22), # ssh_host is IP address of EC2 instance; 22 is the default port number for SSH connections
        ssh_username=ssh_username, # ssh_username is predefined parameters
        ssh_pkey=ssh_private_key,  # ssh_pkey is predefined parameters
        remote_bind_address=(mysql_host, mysql_port)
    ) as tunnel:

        # Create a MySQL engine
        local_port = tunnel.local_bind_port #This port is dynamically assigned when the tunnel is created.
        db_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@127.0.0.1:{local_port}/{mysql_db}"
        db_engine = create_engine(db_url)

        # Load the dataframe into MySQL
        df.to_sql(table_name, db_engine, if_exists='replace', index=False)


if __name__ == "__main__":
	data = extract()
	df = transform(data)
	load(df, table_name='cal_uni')