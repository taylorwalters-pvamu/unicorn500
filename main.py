from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import aiofiles
import shutil
import tempfile
import os
from typing import Annotated
from qvd import qvd_reader
from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.publishing import publish_datasource

#put response codes eventually
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#wrap in if statemnet for if qvd file, else response for incorrect file..........
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(f"Received file: {file.filename}")
    df_read = qvd_reader.read(file.filename)
    df = pd.DataFrame(df_read)
        
    json_data = df.to_json(orient='index') ##df.to_json(r'Path to store the exported JSON file\File Name.json')

    return {json_data}

async def excel_download_file(json_data):
    # Load JSON data into a DataFrame
    df = pd.read_json(json_data)
    
    # Export DataFrame to Excel
    excel_filename = 'data.xlsx'
    async with aiofiles.open(excel_filename, 'wb') as file:
        await file.write(df.to_excel(index=False))

    

async def tableau_publish_dataset(json_data):
    
    tableau_auth = {
        'server': 'YOUR_TABLEAU_SERVER_URL',
        'username': 'YOUR_TABLEAU_USERNAME',
        'password': 'YOUR_TABLEAU_PASSWORD',
        'site': 'YOUR_TABLEAU_SITE',
        'api_version': '3.7'
    }
    
    
    conn = TableauServerConnection(tableau_auth)
    conn.sign_in()
    
    df = pd.DataFrame.from_dict(json_data, orient='index', columns=['Value'])
    
    csv_file_path = 'data.csv'
    df.to_csv(csv_file_path, index_label='Key')
    
    data_source = {
        'name': 'MyDataSource',
        'connection_type': 'textFile',
        'connection_url': csv_file_path,
        'project_id': 'YOUR_PROJECT_ID'
    }
    
    publish_datasource(conn, datasource_dict=data_source)
    print('Data source published successfully!')

    
   