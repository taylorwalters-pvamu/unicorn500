from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import shutil
import tempfile
import os
from typing import Annotated
from qvd import qvd_reader

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

async def json_to_powerbi():


#need to have the json_data hit power bi's endpoint to create a dataset
#route for the batch processing that you can require a folder or zip for
    
    '''# Create a temporary file to save the uploaded QVD file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_file_path = tmp_file.name
    
    # Now, use qvd_reader to read the QVD file into a pandas DataFrame
    try:
        df_read = qvd_reader.read(tmp_file_path)
        df = pd.DataFrame(df_read)
        
        # Convert the DataFrame into JSON
        json_data = df.to_json(orient="records")
        
        # Clean up the temporary file
        os.unlink(tmp_file_path)
        
        return JSONResponse(content=json_data, media_type="application/json")
    except Exception as e:
     os.unlink(tmp_file_path)
     print(f"Error: {str(e)}")  # Add logging or printing for debugging
     return JSONResponse(content={"error": str(e)}, status_code=500)
     '''