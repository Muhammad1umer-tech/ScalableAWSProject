from dotenv import load_dotenv
import pandas as pd
import psycopg2
import json
import os

load_dotenv()

    
def retrieve_data_from_s3():
    # Read the JSON file
    file_path = os.getenv("CSV_FILE_PATH")
    data = ''
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def check_file():
    file_path = os.getenv("CSV_FILE_PATH")
    df = pd.read_csv(file_path)
    print("check_file: ",df.heads())

def create_db():
    try:
        # Get connection details from environment variables
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DB")
        postgres_endpoint = os.getenv("POSTGRES_ENDPOINT")
        postgres_port = os.getenv("POSTGRES_PORT")
        conn = psycopg2.connect(
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password,
            host=postgres_endpoint,
            port=postgres_port)
        
        cursor = conn.cursor()
        
        # Step 1: Create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS data (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        );
        """
        cursor.execute(create_table_query)
        
        #Step 2: Add data
        datas = retrieve_data_from_s3()
        insert_query = "INSERT INTO data (question, answer) VALUES (%s, %s)"
        for item in datas:
            for question, answer in item.items():
                print(question)
                cursor.execute(insert_query, (question, answer))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print("Error while inserting to database: ",e)


def input_to_response(question):
    try:
        # Get connection details from environment variables
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_db = os.getenv("POSTGRES_DB")
        postgres_endpoint = os.getenv("POSTGRES_ENDPOINT")
        postgres_port = os.getenv("POSTGRES_PORT")
        conn = psycopg2.connect(
            dbname=postgres_db,
            user=postgres_user,
            password=postgres_password,
            host=postgres_endpoint,
            port=postgres_port)
        
        cursor = conn.cursor()
        
        select_query = "SELECT answer FROM data WHERE question = %s"
        cursor.execute(select_query, (question,))

        # Fetch the result
        result = cursor.fetchone()
        print(result)
        if result:
            return result[0]
        else:
            return "Question not found in the database."
    except Exception as e:
        print("Error while retrieving data from DB", e)
        return "Error while retrieving data from DB"


# create_db()    
input_to_response("are you familiar with python")
