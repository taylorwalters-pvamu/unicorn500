from fastapi import FastAPI, File, UploadFile,  HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Annotated
import shutil
import tempfile
import os
import sys
import time
import asyncio
import json
from qvd import qvd_reader

#put response codes eventually
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}    

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    try:
        return qvd_to_json(file)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"ValueError: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def qvd_to_json(file:UploadFile):
    print(f"Received file: {file.filename}")
    df_read = qvd_reader.read(file.filename)
    df = pd.DataFrame(df_read)
        
    json_data = df.to_json(orient='index') ##df.to_json(r'Path to store the exported JSON file\File Name.json')

    return json_data


"""
In order to create a table in Power BI, we first need all of the columns and their data types.
"""
@app.post("/json_to_powerbi/")
async def json_to_pbi_dataset(json_data: str):
    try:
        original_data = json.loads(json_data)
        first_row = next(iter(original_data.values()))

        def infer_data_type(value):
            if isinstance(value, int):
                return "Int64"
            elif isinstance(value, float):
                return "Double"
            elif isinstance(value, bool):
                return "bool"
            elif isinstance(value, str):
                try:
                    float(value)
                    return "Double" if "." in value else "Int64"
                except ValueError:
                    return "DataTime" if "-" in value else "string"
            else:
                return "Unknown"
        
        columns_list = [{"name": key, "dataType": infer_data_type(value)} for key, value in first_row.items()]

        transformed_data = {
            "name": "Orders", ## need to change this to infered from file name
            "defaultMode": "Push",
            "tables": [
                {
                    "name": "Table1",  ## need to change this to user input
                    "columns": columns_list
                }
            ]
        }

        transformed_json_data = json.dumps(transformed_data, indent=4)
        return transformed_json_data

    except json.JSONDecodeError as e:
        print("There was an error decoding the JSON:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
