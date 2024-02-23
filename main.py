from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import shutil
import tempfile
import os
from qvd import qvd_reader

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload_file")
async def create_upload_file(file: UploadFile, visualization: str):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            shutil.copyfileobj(file.file, temp)
            temp.flush()
            temp.seek(0)
            df_read = qvd_reader.read(temp.name)
            df = pd.DataFrame(df_read)
            json_data = df.to_json(orient='index')
            json_response = JSONResponse(content=json_data, status_code=200)
            
            if visualization == "power_bi":
                json_to_powerbi(json_response)
            else:
                return {"message": "complete"}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"ValueError: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

async def json_to_powerbi(json_data):


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