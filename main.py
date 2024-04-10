from fastapi import FastAPI, File, UploadFile,  HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from typing import Annotated, List, Dict
import json
from qvd import qvd_reader

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
    print(json_data)
    return json_data

"""
In order to create a table in Power BI, we first need all of the columns and their data types.
"""

class JsonData(BaseModel):
    json_data: str
    dataset_name: str = "Orders"  # Default value if not provided
    table_name: str = "Table1"  # Default value if not provided

@app.post("/json_to_powerbi/")
async def json_to_pbi_dataset(data: JsonData):
    try:
        original_data = json.loads(data.json_data)
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
                    try:
                        # Attempt to parse the string as a date
                        # You might need to adjust this based on your date format
                        datetime.strptime(value, "%d-%m-%Y")
                        return "DateTime"
                    except ValueError:
                        return "string"
            else:
                return "Unknown"
        
        columns_list = [{"name": key, "dataType": infer_data_type(value)} for key, value in first_row.items()]

        transformed_data = {
            "name": data.dataset_name, ## need to change this to infered from file name
            "defaultMode": "Push",
            "tables": [
                {
                    "name": data.table_name,  ## need to change this to user input
                    "columns": columns_list
                }
            ]
        }

        transformed_json_data = json.dumps(transformed_data)    
        return transformed_json_data

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


@app.post("/format_for_powerbi/")
async def format_for_powerbi(json_data: str):
    try:
        original_data = json.loads(json_data)
        print(original_data)
    
        if not isinstance(original_data, dict):
            raise ValueError("Input data is not a valid JSON object.")
        
        rows_list = []
        for item in original_data.values():
            row = {key: convert_value(value) for key, value in item.items()}
            rows_list.append(row)
        
        transformed_data = {"rows": rows_list}
        return json.dumps(transformed_data)

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Error decoding JSON: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

def convert_value(value):
    """
    Attempt to convert string values to their appropriate data types.
    """
    if isinstance(value, str):
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return value
    else:
        return value

#response into variables (need to save for making rows)
#post request for creating rows from json data
